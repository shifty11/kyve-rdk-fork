import { DataItem, IRuntime, Validator } from '@kyvejs/protocol';
import { name, version } from '../package.json';
import axios from 'axios';

// TendermintBSync config
interface IConfig {
  api: string;
  interval: number;
}

interface ISnapshot {
  height: number;
  format: number;
  chunks: number;
  hash: string;
  metadata: string;
}

export default class TendermintSSync implements IRuntime {
  public name = name;
  public version = version;
  public config!: IConfig;

  async validateSetConfig(rawConfig: string): Promise<void> {
    const config: IConfig = JSON.parse(rawConfig);

    if (!config.api) {
      throw new Error(`Config does not have property "api" defined`);
    }

    if (!config.interval) {
      throw new Error(`Config does not have property "interval" defined`);
    }

    if (process.env.KYVEJS_TENDERMINT_SSYNC_API) {
      config.api = process.env.KYVEJS_TENDERMINT_SSYNC_API;
    }

    this.config = config;
  }

  async getDataItem(_: Validator, key: string): Promise<DataItem> {
    // fetch snapshot chunk from given height, format and chunk derived from key
    const [height, __, chunkIndex] = key.split('/').map((k) => +k);

    const { data: snapshots } = await axios.get(
      `${this.config.api}/list_snapshots`
    );

    if (!snapshots) {
      throw new Error(`404: Snapshot with height ${height} not found`);
    }

    const snapshot: ISnapshot = snapshots.find(
      (s: ISnapshot) => s.height === height
    );

    if (!snapshot) {
      throw new Error(`404: Snapshot with height ${height} not found`);
    }

    const { data: chunk } = await axios.get(
      `${this.config.api}/load_snapshot_chunk/${height}/${snapshot.format}/${chunkIndex}`
    );

    // TODO: include trusted app_hash
    return {
      key,
      value: {
        snapshot,
        chunkIndex,
        chunk,
      },
    };
  }

  async prevalidateDataItem(_: Validator, item: DataItem): Promise<boolean> {
    // check if block is defined
    if (!item.value) {
      return false;
    }

    return true;
  }

  async transformDataItem(_: Validator, item: DataItem): Promise<DataItem> {
    // don't transform data item
    return item;
  }

  async validateDataItem(
    _: Validator,
    proposedDataItem: DataItem,
    validationDataItem: DataItem
  ): Promise<boolean> {
    // apply equal comparison
    return (
      JSON.stringify(proposedDataItem) === JSON.stringify(validationDataItem)
    );
  }

  async summarizeDataBundle(_: Validator, bundle: DataItem[]): Promise<string> {
    // TODO: maybe app hash or snapshot hash?
    return `${bundle.at(-1)?.value?.snapshot?.height ?? '0'}/${
      bundle.at(-1)?.value?.chunkIndex
    }`;
  }

  async nextKey(_: Validator, key: string): Promise<string> {
    const [height, chunks, chunkIndex] = key.split('/').map((k) => +k);

    // move on to next snapshot and start at first chunk
    // if we have already reached all chunks in current snapshot
    if (chunks - 1 === chunkIndex) {
      const { data: snapshots } = await axios.get(
        `${this.config.api}/list_snapshots`
      );

      const nextHeight = height + this.config.interval;

      if (!snapshots) {
        throw new Error(`404: Snapshot with height ${nextHeight} not found`);
      }

      const snapshot: ISnapshot = snapshots.find(
        (s: ISnapshot) => s.height === height
      );

      if (!snapshot) {
        throw new Error(`404: Snapshot with height ${nextHeight} not found`);
      }

      // continue with new snapshot height and start at chunk index zero
      return `${snapshot.height}/${snapshot.chunks}/0`;
    }

    // if there are still chunks left in the snapshot we increase
    // the chunk index
    return `${height}/${chunks}/${chunkIndex + 1}`;
  }
}

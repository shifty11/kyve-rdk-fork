import * as grpc from "@grpc/grpc-js";

export interface ProtocolConfig {
  host: string;
  port: number;
  useGrpc: boolean;
  channelOverride: grpc.Channel | undefined;
}

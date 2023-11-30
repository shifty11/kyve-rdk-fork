# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: kyverdk/runtime/v1/runtime.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
)

import betterproto
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase

from ....kyve.bundles import v1beta1 as ___kyve_bundles_v1_beta1__


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


@dataclass(eq=False, repr=False)
class DataItem(betterproto.Message):
    """
    The main data entity served by the gRPC service Contains the block key and
    the block value as a serialized value
    """

    key: str = betterproto.string_field(1)
    """The key of the data item"""

    value: str = betterproto.string_field(2)
    """The value of the data item"""


@dataclass(eq=False, repr=False)
class RuntimeConfig(betterproto.Message):
    """
    Configuration entity containing serialized info about connection to the
    respective chain
    """

    serialized_config: str = betterproto.string_field(1)
    """The serialized configuration"""


@dataclass(eq=False, repr=False)
class GetRuntimeNameRequest(betterproto.Message):
    """
    GetRuntimeNameRequest Request returning the name of the runtime returns the
    runtime name as a string
    """

    pass


@dataclass(eq=False, repr=False)
class GetRuntimeNameResponse(betterproto.Message):
    """
    GetRuntimeNameResponse Response returning the name of the runtime returns
    the runtime name as a string
    """

    name: str = betterproto.string_field(1)
    """The name of the runtime"""


@dataclass(eq=False, repr=False)
class GetRuntimeVersionRequest(betterproto.Message):
    """
    GetRuntimeVersionRequest Request returning the version of the runtime
    returns the runtime version as a string
    """

    pass


@dataclass(eq=False, repr=False)
class GetRuntimeVersionResponse(betterproto.Message):
    """
    GetRuntimeVersionResponse Response returning the version of the runtime
    returns the runtime version as a string
    """

    version: str = betterproto.string_field(1)
    """The version of the runtime"""


@dataclass(eq=False, repr=False)
class ValidateSetConfigRequest(betterproto.Message):
    """
    ValidateSetConfigRequest Request validating a configuration string to
    connect to the respective chain returns a validated serialized
    configuration object
    """

    raw_config: str = betterproto.string_field(1)
    """The raw configuration string"""


@dataclass(eq=False, repr=False)
class ValidateSetConfigResponse(betterproto.Message):
    """
    ValidateSetConfigResponse Response validating a configuration string to
    connect to the respective chain returns a validated serialized
    configuration object
    """

    serialized_config: str = betterproto.string_field(1)
    """The validated serialized configuration object"""


@dataclass(eq=False, repr=False)
class GetDataItemRequest(betterproto.Message):
    """
    GetDataItemRequest Request retrieving and returning a block from the
    respective chain Returns the requested block as a dataItem
    """

    config: "RuntimeConfig" = betterproto.message_field(1)
    """The configuration object"""

    key: str = betterproto.string_field(2)
    """The key of the data item"""


@dataclass(eq=False, repr=False)
class GetDataItemResponse(betterproto.Message):
    """
    GetDataItemResponse Response retrieving and returning a block from the
    respective chain Returns the requested block as a dataItem
    """

    data_item: "DataItem" = betterproto.message_field(1)
    """The data item"""


@dataclass(eq=False, repr=False)
class PrevalidateDataItemRequest(betterproto.Message):
    """
    PrevalidateDataItemRequest Request pre-validating a dataItem that is about
    to be validated returns the pre-validation result as a boolean
    """

    config: "RuntimeConfig" = betterproto.message_field(1)
    """The configuration object"""

    data_item: "DataItem" = betterproto.message_field(2)
    """The data item to be pre-validated"""


@dataclass(eq=False, repr=False)
class PrevalidateDataItemResponse(betterproto.Message):
    """
    PrevalidateDataItemResponse Response pre-validating a dataItem that is
    about to be validated returns the pre-validation result as a boolean
    """

    valid: bool = betterproto.bool_field(1)
    """The pre-validation result"""

    error: str = betterproto.string_field(2)
    """The pre-validation error message"""


@dataclass(eq=False, repr=False)
class TransformDataItemRequest(betterproto.Message):
    """
    TransformDataItemRequest Request transforming the given data item into a
    preferred format returns the transformed dataItem
    """

    config: "RuntimeConfig" = betterproto.message_field(1)
    """The configuration object"""

    data_item: "DataItem" = betterproto.message_field(2)
    """The data item to be transformed"""


@dataclass(eq=False, repr=False)
class TransformDataItemResponse(betterproto.Message):
    """
    TransformDataItemResponse Response transforming the given data item into a
    preferred format returns the transformed dataItem
    """

    transformed_data_item: "DataItem" = betterproto.message_field(1)
    """The transformed data item"""


@dataclass(eq=False, repr=False)
class ValidateDataItemRequest(betterproto.Message):
    """
    ValidateDataItemRequest Request validating a dataItem returns the
    validation result as a boolean
    """

    config: "RuntimeConfig" = betterproto.message_field(1)
    """The configuration object"""

    proposed_data_item: "DataItem" = betterproto.message_field(2)
    """The proposed data item"""

    validation_data_item: "DataItem" = betterproto.message_field(3)
    """The data item to be validated"""


@dataclass(eq=False, repr=False)
class ValidateDataItemResponse(betterproto.Message):
    """
    ValidateDataItemResponse Response validating a dataItem returns the
    validation result as a boolean
    """

    vote: "___kyve_bundles_v1_beta1__.VoteType" = betterproto.enum_field(1)
    """The validation result as vote"""


@dataclass(eq=False, repr=False)
class SummarizeDataBundleRequest(betterproto.Message):
    """
    SummarizeDataBundleRequest Request summarizing a dataBundle returns the
    bundle summary as a string
    """

    config: "RuntimeConfig" = betterproto.message_field(1)
    """The configuration object"""

    bundle: List["DataItem"] = betterproto.message_field(2)
    """The data items to be summarized"""


@dataclass(eq=False, repr=False)
class SummarizeDataBundleResponse(betterproto.Message):
    """
    SummarizeDataBundleResponse Response summarizing a dataBundle returns the
    bundle summary as a string
    """

    summary: str = betterproto.string_field(1)
    """The bundle summary"""


@dataclass(eq=False, repr=False)
class NextKeyRequest(betterproto.Message):
    """
    NextKeyRequest Request retrieving the next key on the chain returns the key
    as a string
    """

    config: "RuntimeConfig" = betterproto.message_field(1)
    """The configuration object"""

    key: str = betterproto.string_field(2)
    """The current key"""


@dataclass(eq=False, repr=False)
class NextKeyResponse(betterproto.Message):
    """
    NextKeyResponse Response retrieving the next key on the chain returns the
    key as a string
    """

    next_key: str = betterproto.string_field(1)
    """The next key"""


class RuntimeServiceStub(betterproto.ServiceStub):
    async def get_runtime_name(
        self,
        get_runtime_name_request: "GetRuntimeNameRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "GetRuntimeNameResponse":
        return await self._unary_unary(
            "/kyverdk.runtime.v1.RuntimeService/GetRuntimeName",
            get_runtime_name_request,
            GetRuntimeNameResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_runtime_version(
        self,
        get_runtime_version_request: "GetRuntimeVersionRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "GetRuntimeVersionResponse":
        return await self._unary_unary(
            "/kyverdk.runtime.v1.RuntimeService/GetRuntimeVersion",
            get_runtime_version_request,
            GetRuntimeVersionResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def validate_set_config(
        self,
        validate_set_config_request: "ValidateSetConfigRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ValidateSetConfigResponse":
        return await self._unary_unary(
            "/kyverdk.runtime.v1.RuntimeService/ValidateSetConfig",
            validate_set_config_request,
            ValidateSetConfigResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def get_data_item(
        self,
        get_data_item_request: "GetDataItemRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "GetDataItemResponse":
        return await self._unary_unary(
            "/kyverdk.runtime.v1.RuntimeService/GetDataItem",
            get_data_item_request,
            GetDataItemResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def prevalidate_data_item(
        self,
        prevalidate_data_item_request: "PrevalidateDataItemRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "PrevalidateDataItemResponse":
        return await self._unary_unary(
            "/kyverdk.runtime.v1.RuntimeService/PrevalidateDataItem",
            prevalidate_data_item_request,
            PrevalidateDataItemResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def transform_data_item(
        self,
        transform_data_item_request: "TransformDataItemRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "TransformDataItemResponse":
        return await self._unary_unary(
            "/kyverdk.runtime.v1.RuntimeService/TransformDataItem",
            transform_data_item_request,
            TransformDataItemResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def validate_data_item(
        self,
        validate_data_item_request: "ValidateDataItemRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ValidateDataItemResponse":
        return await self._unary_unary(
            "/kyverdk.runtime.v1.RuntimeService/ValidateDataItem",
            validate_data_item_request,
            ValidateDataItemResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def summarize_data_bundle(
        self,
        summarize_data_bundle_request: "SummarizeDataBundleRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "SummarizeDataBundleResponse":
        return await self._unary_unary(
            "/kyverdk.runtime.v1.RuntimeService/SummarizeDataBundle",
            summarize_data_bundle_request,
            SummarizeDataBundleResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def next_key(
        self,
        next_key_request: "NextKeyRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "NextKeyResponse":
        return await self._unary_unary(
            "/kyverdk.runtime.v1.RuntimeService/NextKey",
            next_key_request,
            NextKeyResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class RuntimeServiceBase(ServiceBase):
    async def get_runtime_name(
        self, get_runtime_name_request: "GetRuntimeNameRequest"
    ) -> "GetRuntimeNameResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_runtime_version(
        self, get_runtime_version_request: "GetRuntimeVersionRequest"
    ) -> "GetRuntimeVersionResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def validate_set_config(
        self, validate_set_config_request: "ValidateSetConfigRequest"
    ) -> "ValidateSetConfigResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def get_data_item(
        self, get_data_item_request: "GetDataItemRequest"
    ) -> "GetDataItemResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def prevalidate_data_item(
        self, prevalidate_data_item_request: "PrevalidateDataItemRequest"
    ) -> "PrevalidateDataItemResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def transform_data_item(
        self, transform_data_item_request: "TransformDataItemRequest"
    ) -> "TransformDataItemResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def validate_data_item(
        self, validate_data_item_request: "ValidateDataItemRequest"
    ) -> "ValidateDataItemResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def summarize_data_bundle(
        self, summarize_data_bundle_request: "SummarizeDataBundleRequest"
    ) -> "SummarizeDataBundleResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def next_key(self, next_key_request: "NextKeyRequest") -> "NextKeyResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_get_runtime_name(
        self,
        stream: "grpclib.server.Stream[GetRuntimeNameRequest, GetRuntimeNameResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_runtime_name(request)
        await stream.send_message(response)

    async def __rpc_get_runtime_version(
        self,
        stream: "grpclib.server.Stream[GetRuntimeVersionRequest, GetRuntimeVersionResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_runtime_version(request)
        await stream.send_message(response)

    async def __rpc_validate_set_config(
        self,
        stream: "grpclib.server.Stream[ValidateSetConfigRequest, ValidateSetConfigResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.validate_set_config(request)
        await stream.send_message(response)

    async def __rpc_get_data_item(
        self, stream: "grpclib.server.Stream[GetDataItemRequest, GetDataItemResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.get_data_item(request)
        await stream.send_message(response)

    async def __rpc_prevalidate_data_item(
        self,
        stream: "grpclib.server.Stream[PrevalidateDataItemRequest, PrevalidateDataItemResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.prevalidate_data_item(request)
        await stream.send_message(response)

    async def __rpc_transform_data_item(
        self,
        stream: "grpclib.server.Stream[TransformDataItemRequest, TransformDataItemResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.transform_data_item(request)
        await stream.send_message(response)

    async def __rpc_validate_data_item(
        self,
        stream: "grpclib.server.Stream[ValidateDataItemRequest, ValidateDataItemResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.validate_data_item(request)
        await stream.send_message(response)

    async def __rpc_summarize_data_bundle(
        self,
        stream: "grpclib.server.Stream[SummarizeDataBundleRequest, SummarizeDataBundleResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.summarize_data_bundle(request)
        await stream.send_message(response)

    async def __rpc_next_key(
        self, stream: "grpclib.server.Stream[NextKeyRequest, NextKeyResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.next_key(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/kyverdk.runtime.v1.RuntimeService/GetRuntimeName": grpclib.const.Handler(
                self.__rpc_get_runtime_name,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetRuntimeNameRequest,
                GetRuntimeNameResponse,
            ),
            "/kyverdk.runtime.v1.RuntimeService/GetRuntimeVersion": grpclib.const.Handler(
                self.__rpc_get_runtime_version,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetRuntimeVersionRequest,
                GetRuntimeVersionResponse,
            ),
            "/kyverdk.runtime.v1.RuntimeService/ValidateSetConfig": grpclib.const.Handler(
                self.__rpc_validate_set_config,
                grpclib.const.Cardinality.UNARY_UNARY,
                ValidateSetConfigRequest,
                ValidateSetConfigResponse,
            ),
            "/kyverdk.runtime.v1.RuntimeService/GetDataItem": grpclib.const.Handler(
                self.__rpc_get_data_item,
                grpclib.const.Cardinality.UNARY_UNARY,
                GetDataItemRequest,
                GetDataItemResponse,
            ),
            "/kyverdk.runtime.v1.RuntimeService/PrevalidateDataItem": grpclib.const.Handler(
                self.__rpc_prevalidate_data_item,
                grpclib.const.Cardinality.UNARY_UNARY,
                PrevalidateDataItemRequest,
                PrevalidateDataItemResponse,
            ),
            "/kyverdk.runtime.v1.RuntimeService/TransformDataItem": grpclib.const.Handler(
                self.__rpc_transform_data_item,
                grpclib.const.Cardinality.UNARY_UNARY,
                TransformDataItemRequest,
                TransformDataItemResponse,
            ),
            "/kyverdk.runtime.v1.RuntimeService/ValidateDataItem": grpclib.const.Handler(
                self.__rpc_validate_data_item,
                grpclib.const.Cardinality.UNARY_UNARY,
                ValidateDataItemRequest,
                ValidateDataItemResponse,
            ),
            "/kyverdk.runtime.v1.RuntimeService/SummarizeDataBundle": grpclib.const.Handler(
                self.__rpc_summarize_data_bundle,
                grpclib.const.Cardinality.UNARY_UNARY,
                SummarizeDataBundleRequest,
                SummarizeDataBundleResponse,
            ),
            "/kyverdk.runtime.v1.RuntimeService/NextKey": grpclib.const.Handler(
                self.__rpc_next_key,
                grpclib.const.Cardinality.UNARY_UNARY,
                NextKeyRequest,
                NextKeyResponse,
            ),
        }
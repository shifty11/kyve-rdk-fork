// This is the entry point for the protocol if used with grpc (within docker)
import { ProtocolConfig } from "./types";
import { Validator } from "./index";

const config: Partial<ProtocolConfig> = {
  host: process.env.HOST || "locahost",
  port: parseInt(process.env.PORT || "50051"),
};
new Validator(config).bootstrap();

// This file is auto-generated, don't edit it
import * as $dara from "@darabonba/typescript";

export class CreateMcpSessionRequest extends $dara.Model {
  authorization?: string;
  contextId?: string;
  externalUserId?: string;
  imageId?: string;
  labels?: string;
  sessionId?: string;
  static names(): { [key: string]: string } {
    return {
      authorization: "Authorization",
      contextId: "ContextId",
      externalUserId: "ExternalUserId",
      imageId: "ImageId",
      labels: "Labels",
      sessionId: "SessionId",
    };
  }

  static types(): { [key: string]: any } {
    return {
      authorization: "string",
      contextId: "string",
      externalUserId: "string",
      imageId: "string",
      labels: "string",
      sessionId: "string",
    };
  }

  validate() {
    super.validate();
  }

  constructor(map?: { [key: string]: any }) {
    super(map);
  }
}

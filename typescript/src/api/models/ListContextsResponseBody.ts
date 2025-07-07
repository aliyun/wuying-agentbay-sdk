// This file is auto-generated, don't edit it
import * as $dara from "@darabonba/typescript";
import { ListContextsResponseBodyData } from "./ListContextsResponseBodyData";

export class ListContextsResponseBody extends $dara.Model {
  code?: string;
  data?: ListContextsResponseBodyData[];
  httpStatusCode?: number;
  maxResults?: number;
  message?: string;
  nextToken?: string;
  requestId?: string;
  success?: boolean;
  totalCount?: number;
  static names(): { [key: string]: string } {
    return {
      code: "Code",
      data: "Data",
      httpStatusCode: "HttpStatusCode",
      maxResults: "MaxResults",
      message: "Message",
      nextToken: "NextToken",
      requestId: "RequestId",
      success: "Success",
      totalCount: "TotalCount",
    };
  }

  static types(): { [key: string]: any } {
    return {
      code: "string",
      data: { type: "array", itemType: ListContextsResponseBodyData },
      httpStatusCode: "number",
      maxResults: "number",
      message: "string",
      nextToken: "string",
      requestId: "string",
      success: "boolean",
      totalCount: "number",
    };
  }

  validate() {
    if (Array.isArray(this.data)) {
      $dara.Model.validateArray(this.data);
    }
    super.validate();
  }

  constructor(map?: { [key: string]: any }) {
    super(map);
  }
}

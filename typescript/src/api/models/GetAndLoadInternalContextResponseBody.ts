// This file is auto-generated, don't edit it
import * as $dara from '@darabonba/typescript';


export class GetAndLoadInternalContextResponseBodyData extends $dara.Model {
  contextId?: string;
  contextPath?: string;
  contextType?: string;
  static names(): { [key: string]: string } {
    return {
      contextId: 'ContextId',
      contextPath: 'ContextPath',
      contextType: 'ContextType',
    };
  }

  static types(): { [key: string]: any } {
    return {
      contextId: 'string',
      contextPath: 'string',
      contextType: 'string',
    };
  }

  validate() {
    super.validate();
  }

  constructor(map?: { [key: string]: any }) {
    super(map);
  }
}

export class GetAndLoadInternalContextResponseBody extends $dara.Model {
  code?: string;
  data?: GetAndLoadInternalContextResponseBodyData[];
  httpStatusCode?: number;
  message?: string;
  requestId?: string;
  success?: boolean;
  static names(): { [key: string]: string } {
    return {
      code: 'Code',
      data: 'Data',
      httpStatusCode: 'HttpStatusCode',
      message: 'Message',
      requestId: 'RequestId',
      success: 'Success',
    };
  }

  static types(): { [key: string]: any } {
    return {
      code: 'string',
      data: { 'type': 'array', 'itemType': GetAndLoadInternalContextResponseBodyData },
      httpStatusCode: 'number',
      message: 'string',
      requestId: 'string',
      success: 'boolean',
    };
  }

  validate() {
    if(Array.isArray(this.data)) {
      $dara.Model.validateArray(this.data);
    }
    super.validate();
  }

  constructor(map?: { [key: string]: any }) {
    super(map);
  }
}


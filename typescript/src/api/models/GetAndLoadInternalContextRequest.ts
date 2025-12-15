// This file is auto-generated, don't edit it
import * as $dara from '@darabonba/typescript';


export class GetAndLoadInternalContextRequest extends $dara.Model {
  authorization?: string;
  contextTypes?: string[];
  sessionId?: string;
  static names(): { [key: string]: string } {
    return {
      authorization: 'Authorization',
      contextTypes: 'ContextTypes',
      sessionId: 'SessionId',
    };
  }

  static types(): { [key: string]: any } {
    return {
      authorization: 'string',
      contextTypes: { 'type': 'array', 'itemType': 'string' },
      sessionId: 'string',
    };
  }

  validate() {
    if(Array.isArray(this.contextTypes)) {
      $dara.Model.validateArray(this.contextTypes);
    }
    super.validate();
  }

  constructor(map?: { [key: string]: any }) {
    super(map);
  }
}


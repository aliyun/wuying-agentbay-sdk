// This file is auto-generated, don't edit it
import * as $dara from '@darabonba/typescript';


export class GetSessionResponseBodyData extends $dara.Model {
  appInstanceId?: string;
  resourceId?: string;
  sessionId?: string;
  success?: boolean;
  static names(): { [key: string]: string } {
    return {
      appInstanceId: 'AppInstanceId',
      resourceId: 'ResourceId',
      sessionId: 'SessionId',
      success: 'Success',
    };
  }

  static types(): { [key: string]: any } {
    return {
      appInstanceId: 'string',
      resourceId: 'string',
      sessionId: 'string',
      success: 'boolean',
    };
  }

  validate() {
    super.validate();
  }

  constructor(map?: { [key: string]: any }) {
    super(map);
  }
}


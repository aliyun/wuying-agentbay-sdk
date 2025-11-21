// This file is auto-generated, don't edit it. Thanks.
package com.aliyun.wuyingai20250506.models;

import com.aliyun.tea.*;

public class DescribeNetworkRequest extends TeaModel {
    @NameInMap("Authorization")
    public String authorization;

    @NameInMap("NetworkId")
    public String networkId;

    public static DescribeNetworkRequest build(java.util.Map<String, ?> map) throws Exception {
        DescribeNetworkRequest self = new DescribeNetworkRequest();
        return TeaModel.build(map, self);
    }

    public DescribeNetworkRequest setAuthorization(String authorization) {
        this.authorization = authorization;
        return this;
    }
    public String getAuthorization() {
        return this.authorization;
    }

    public DescribeNetworkRequest setNetworkId(String networkId) {
        this.networkId = networkId;
        return this;
    }
    public String getNetworkId() {
        return this.networkId;
    }

}

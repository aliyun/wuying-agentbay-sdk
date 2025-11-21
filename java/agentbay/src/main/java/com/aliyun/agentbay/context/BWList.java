package com.aliyun.agentbay.context;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Defines the black and white list configuration
 */
public class BWList {
    private List<WhiteList> whiteLists = new ArrayList<>();

    public BWList() {
    }

    public BWList(List<WhiteList> whiteLists) {
        this.whiteLists = whiteLists != null ? whiteLists : new ArrayList<>();
    }

    public List<WhiteList> getWhiteLists() {
        return whiteLists;
    }

    public void setWhiteLists(List<WhiteList> whiteLists) {
        this.whiteLists = whiteLists != null ? whiteLists : new ArrayList<>();
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        List<Map<String, Object>> whiteListMaps = whiteLists.stream()
                .map(WhiteList::toMap)
                .collect(Collectors.toList());
        map.put("whiteLists", whiteListMaps);
        return map;
    }
}
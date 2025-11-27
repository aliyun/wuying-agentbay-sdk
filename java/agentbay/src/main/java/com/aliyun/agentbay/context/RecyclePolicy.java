package com.aliyun.agentbay.context;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * Defines the recycle policy for context synchronization
 * 
 * Attributes:
 *     lifecycle: Defines how long the context data should be retained
 *         Available options:
 *         - LIFECYCLE_1DAY: Keep data for 1 day
 *         - LIFECYCLE_3DAYS: Keep data for 3 days
 *         - LIFECYCLE_5DAYS: Keep data for 5 days
 *         - LIFECYCLE_10DAYS: Keep data for 10 days
 *         - LIFECYCLE_15DAYS: Keep data for 15 days
 *         - LIFECYCLE_30DAYS: Keep data for 30 days
 *         - LIFECYCLE_90DAYS: Keep data for 90 days
 *         - LIFECYCLE_180DAYS: Keep data for 180 days
 *         - LIFECYCLE_360DAYS: Keep data for 360 days
 *         - LIFECYCLE_FOREVER: Keep data permanently (default)
 *     paths: Specifies which directories or files should be subject to the recycle policy
 *         Rules:
 *         - Must use exact directory/file paths
 *         - Wildcard patterns (* ? [ ]) are NOT supported
 *         - Empty string "" means apply to all paths in the context
 *         - Multiple paths can be specified as a list
 *         Default: [""] (applies to all paths)
 */
public class RecyclePolicy {
    private static final Pattern WILDCARD_PATTERN = Pattern.compile("[*?\\[\\]]");
    
    private Lifecycle lifecycle = Lifecycle.LIFECYCLE_FOREVER;
    private List<String> paths = new ArrayList<>(Arrays.asList(""));

    public RecyclePolicy() {
        this.lifecycle = Lifecycle.LIFECYCLE_FOREVER;
        this.paths = new ArrayList<>(Arrays.asList(""));
    }

    public RecyclePolicy(Lifecycle lifecycle, List<String> paths) {
        this.lifecycle = lifecycle != null ? lifecycle : Lifecycle.LIFECYCLE_FOREVER;
        this.paths = paths != null ? new ArrayList<>(paths) : new ArrayList<>(Arrays.asList(""));
        
        // Validate lifecycle and paths
        validate();
    }

    /**
     * Validate lifecycle and paths configuration
     * 
     * @throws IllegalArgumentException if validation fails
     */
    public void validate() {
        // Validate lifecycle value
        if (lifecycle == null) {
            throw new IllegalArgumentException("Lifecycle cannot be null");
        }
        
        // Validate that paths don't contain wildcard patterns
        for (String path : paths) {
            if (path != null && !path.trim().isEmpty() && containsWildcard(path)) {
                throw new IllegalArgumentException(
                    "Wildcard patterns are not supported in recycle policy paths. Got: " + path + ". " +
                    "Please use exact directory paths instead."
                );
            }
        }
    }

    /**
     * Check if path contains wildcard characters
     * 
     * @param path path to check
     * @return true if path contains wildcards, false otherwise
     */
    private static boolean containsWildcard(String path) {
        return WILDCARD_PATTERN.matcher(path).find();
    }

    /**
     * Creates a new recycle policy with default values
     * 
     * @return RecyclePolicy with default values
     */
    public static RecyclePolicy defaultPolicy() {
        return new RecyclePolicy();
    }

    public Lifecycle getLifecycle() {
        return lifecycle;
    }

    public void setLifecycle(Lifecycle lifecycle) {
        if (lifecycle == null) {
            throw new IllegalArgumentException("Lifecycle cannot be null");
        }
        this.lifecycle = lifecycle;
    }

    public List<String> getPaths() {
        return new ArrayList<>(paths);
    }

    public void setPaths(List<String> paths) {
        this.paths = paths != null ? new ArrayList<>(paths) : new ArrayList<>(Arrays.asList(""));
        // Validate paths after setting
        for (String path : this.paths) {
            if (path != null && !path.trim().isEmpty() && containsWildcard(path)) {
                throw new IllegalArgumentException(
                    "Wildcard patterns are not supported in recycle policy paths. Got: " + path
                );
            }
        }
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("lifecycle", lifecycle != null ? lifecycle.getValue() : null);
        map.put("paths", new ArrayList<>(paths));
        return map;
    }
}


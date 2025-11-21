package com.aliyun.agentbay.browser;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.module.jsonSchema.JsonSchema;
import com.fasterxml.jackson.module.jsonSchema.JsonSchemaGenerator;

import java.util.HashMap;
import java.util.Map;

/**
 * Options for browser extract operations - matches Python ExtractOptions
 * Generic type T represents the schema/result type (similar to Python's Generic[T])
 */
public class ExtractOptions<T> {
    private String instruction;
    private Class<T> schema;
    private String schemaJson;
    private Boolean useTextExtract;
    private String selector;
    private Boolean iframe;
    private Integer domSettleTimeoutMs;
    private Boolean useVision;

    public ExtractOptions(String instruction, Class<T> schema) {
        this.instruction = instruction;
        this.schema = schema;
    }

    public ExtractOptions(String instruction, String schemaJson) {
        this.instruction = instruction;
        this.schemaJson = schemaJson;
    }

    public ExtractOptions(String instruction, Class<T> schema, Boolean useTextExtract, String selector,
                         Boolean iframe, Integer domSettleTimeoutMs, Boolean useVision) {
        this.instruction = instruction;
        this.schema = schema;
        this.useTextExtract = useTextExtract;
        this.selector = selector;
        this.iframe = iframe;
        this.domSettleTimeoutMs = domSettleTimeoutMs;
        this.useVision = useVision;
    }

    public Map<String, Object> toMap() {
        Map<String, Object> map = new HashMap<>();
        map.put("instruction", instruction);

        if (schemaJson != null) {
            map.put("field_schema", "schema: " + schemaJson);
        } else if (schema != null) {
            try {
                ObjectMapper mapper = new ObjectMapper();
                JsonSchemaGenerator schemaGen = new JsonSchemaGenerator(mapper);
                JsonSchema jsonSchema = schemaGen.generateSchema(schema);
                String schemaStr = mapper.writeValueAsString(jsonSchema);
                map.put("field_schema", "schema: " + schemaStr);
            } catch (Exception e) {
                throw new RuntimeException("Failed to generate schema from class: " + e.getMessage(), e);
            }
        }

        if (useTextExtract != null) map.put("use_text_extract", useTextExtract);
        if (selector != null) map.put("selector", selector);
        if (iframe != null) map.put("iframe", iframe);
        if (domSettleTimeoutMs != null) map.put("dom_settle_timeout_ms", domSettleTimeoutMs);
        if (useVision != null) map.put("use_vision", useVision);
        return map;
    }

    // Getters and setters
    public String getInstruction() { return instruction; }
    public void setInstruction(String instruction) { this.instruction = instruction; }

    public Class<T> getSchema() { return schema; }
    public void setSchema(Class<T> schema) { this.schema = schema; }

    public String getSchemaJson() { return schemaJson; }
    public void setSchemaJson(String schemaJson) { this.schemaJson = schemaJson; }

    public Boolean getUseTextExtract() { return useTextExtract; }
    public void setUseTextExtract(Boolean useTextExtract) { this.useTextExtract = useTextExtract; }

    public String getSelector() { return selector; }
    public void setSelector(String selector) { this.selector = selector; }

    public Boolean getIframe() { return iframe; }
    public void setIframe(Boolean iframe) { this.iframe = iframe; }

    public Integer getDomSettleTimeoutMs() { return domSettleTimeoutMs; }
    public void setDomSettleTimeoutMs(Integer domSettleTimeoutMs) { this.domSettleTimeoutMs = domSettleTimeoutMs; }

    public Boolean getUseVision() { return useVision; }
    public void setUseVision(Boolean useVision) { this.useVision = useVision; }
}
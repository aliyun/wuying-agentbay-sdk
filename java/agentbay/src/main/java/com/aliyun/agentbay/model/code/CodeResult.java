package com.aliyun.agentbay.model.code;

import java.util.ArrayList;
import java.util.List;

public class CodeResult {
    private String text;
    private String html;
    private String markdown;
    private String png;
    private String jpeg;
    private String svg;
    private Object json;
    private String latex;
    private Object chart;
    private boolean isMainResult;

    public CodeResult() {
        this.isMainResult = false;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String getHtml() {
        return html;
    }

    public void setHtml(String html) {
        this.html = html;
    }

    public String getMarkdown() {
        return markdown;
    }

    public void setMarkdown(String markdown) {
        this.markdown = markdown;
    }

    public String getPng() {
        return png;
    }

    public void setPng(String png) {
        this.png = png;
    }

    public String getJpeg() {
        return jpeg;
    }

    public void setJpeg(String jpeg) {
        this.jpeg = jpeg;
    }

    public String getSvg() {
        return svg;
    }

    public void setSvg(String svg) {
        this.svg = svg;
    }

    public Object getJson() {
        return json;
    }

    public void setJson(Object json) {
        this.json = json;
    }

    public String getLatex() {
        return latex;
    }

    public void setLatex(String latex) {
        this.latex = latex;
    }

    public Object getChart() {
        return chart;
    }

    public void setChart(Object chart) {
        this.chart = chart;
    }

    public boolean isMainResult() {
        return isMainResult;
    }

    public void setMainResult(boolean mainResult) {
        isMainResult = mainResult;
    }

    public List<String> formats() {
        List<String> formats = new ArrayList<>();
        if (text != null) formats.add("text");
        if (html != null) formats.add("html");
        if (markdown != null) formats.add("markdown");
        if (png != null) formats.add("png");
        if (jpeg != null) formats.add("jpeg");
        if (svg != null) formats.add("svg");
        if (json != null) formats.add("json");
        if (latex != null) formats.add("latex");
        if (chart != null) formats.add("chart");
        return formats;
    }
}

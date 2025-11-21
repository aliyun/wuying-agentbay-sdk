package com.example.agentdemo.controller;

import com.example.agentdemo.service.DataAnalysisService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/agent")
public class AgentController {

    private final DataAnalysisService dataAnalysisService;

    public AgentController(DataAnalysisService dataAnalysisService) {
        this.dataAnalysisService = dataAnalysisService;
    }

    @PostMapping("/analyze")
    public AnalysisResponse analyze(@RequestBody AnalysisRequest request) {
        String result = dataAnalysisService.runAnalysis(request.getPrompt());
        return new AnalysisResponse(result);
    }

    public static class AnalysisRequest {
        private String prompt;

        public String getPrompt() {
            return prompt;
        }

        public void setPrompt(String prompt) {
            this.prompt = prompt;
        }
    }

    public static class AnalysisResponse {
        private String result;

        public AnalysisResponse(String result) {
            this.result = result;
        }

        public String getResult() {
            return result;
        }

        public void setResult(String result) {
            this.result = result;
        }
    }
}

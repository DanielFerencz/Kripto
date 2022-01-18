package client;

import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;
import java.io.*;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.UnrecoverableKeyException;
import java.security.cert.X509Certificate;
import java.util.Arrays;
import java.util.stream.Collectors;

public class Client1 {

    public static final String[] protocols = new String[] {"TLSv1.2"};

    public static final String[] cipher_suites = new String[] {
            "TLS_AES_256_GCM_SHA384",
            "TLS_AES_128_GCM_SHA256",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
            "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384",
            "TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256",
            "TLS_DHE_DSS_WITH_AES_256_GCM_SHA384",
            "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256",
            "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384",
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384",
            "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
            "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256",
            "TLS_DHE_DSS_WITH_AES_256_CBC_SHA256",
            "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256",
            "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256",
            "TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384",
            "TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384",
            "TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256",
            "TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384",
            "TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384",
            "TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256",
            "TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256",
            "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
            "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
            "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
            "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",
            "TLS_DHE_RSA_WITH_AES_256_CBC_SHA",
            "TLS_DHE_DSS_WITH_AES_256_CBC_SHA",
            "TLS_DHE_RSA_WITH_AES_128_CBC_SHA",
            "TLS_DHE_DSS_WITH_AES_128_CBC_SHA",
            "TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA",
            "TLS_ECDH_RSA_WITH_AES_256_CBC_SHA",
            "TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA",
            "TLS_ECDH_RSA_WITH_AES_128_CBC_SHA",
            "TLS_RSA_WITH_AES_256_GCM_SHA384",
            "TLS_RSA_WITH_AES_128_GCM_SHA256",
            "TLS_RSA_WITH_AES_256_CBC_SHA256",
            "TLS_RSA_WITH_AES_128_CBC_SHA256",
            "TLS_RSA_WITH_AES_256_CBC_SHA",
            "TLS_RSA_WITH_AES_128_CBC_SHA",
            "TLS_EMPTY_RENEGOTIATION_INFO_SCSV",
    };

    public  static SSLSocket createSocket(String host, int port) throws IOException, NoSuchAlgorithmException {
        SSLSocket socket = (SSLSocket) SSLSocketFactory.getDefault()
                .createSocket(host, port);
        socket.setNeedClientAuth(true);
        socket.setEnabledProtocols(protocols);
        socket.setEnabledCipherSuites(cipher_suites);
        return socket;
    }

    public static void main(String[] args) throws IOException, KeyStoreException, NoSuchAlgorithmException, UnrecoverableKeyException {


        SSLSocket socket = createSocket("bnr.ro", 443);

        Reader in = new InputStreamReader(socket.getInputStream());
        Writer out = new OutputStreamWriter(socket.getOutputStream());

        out.write("GET /Home.aspx HTTP/1.1\r\n");
        out.write("Host: bnr.ro\r\n");
        out.write("User-Agent: Mozilla/5.0\r\n");
        out.write("Accept: text/xml,application/xml,application/xhtml+xml,text/html*/*\r\n");
        out.write("Accept-Language: en-us\r\n");
        out.write("Connection: keep-alive\r\n");
        out.write("\r\n");
        out.flush();

        char[] data = new char[16384];
        int len = in.read(data);

        if (len <= 0) {
            return;
        }

        String[] lines = (new String(data, 0, len)).split("\r\n");

        String header = Arrays.stream(lines).limit(9).collect(Collectors.joining("\r\n"));
        String body = Arrays.stream(lines).skip(11).collect(Collectors.joining("\r\n"));

        try (BufferedWriter writer = new BufferedWriter(new FileWriter("bnr.header"))) {
            writer.write(header);
        }

        try (BufferedWriter writer = new BufferedWriter(new FileWriter("bnr.html"))) {
            writer.write(body);
        }

        X509Certificate certificate = (X509Certificate) socket.getSession().getPeerCertificates()[0];

        System.out.println("Version nr: " + certificate.getVersion());
        System.out.println("Serial nr: " + certificate.getSerialNumber());
        System.out.println("Issuer: " + certificate.getIssuerDN());
        System.out.println("Valid from: " + certificate.getNotBefore());
        System.out.println("Valid to: " + certificate.getNotAfter());
        System.out.println("Subject: " + certificate.getSubjectDN());
        System.out.println("Valid to: " + certificate.getPublicKey());
    }

}

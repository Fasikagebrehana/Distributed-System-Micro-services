import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = "http://192.168.32.138:5000"; // Replace with your Flask server URL

  // Publish message to RabbitMQ
  Future<void> publishMessage(String routingKey, String message) async {
    final url = Uri.parse("$baseUrl/publish");
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: json.encode({
        "routing_key": routingKey,
        "message": message,
      }),
    );

    if (response.statusCode == 200) {
      print("Message published successfully");
    } else {
      throw Exception("Failed to publish message");
    }
  }

  // Consume messages from RabbitMQ
  // Future<List<String>> consumeMessages() async {
  //   final url = Uri.parse("$baseUrl/consume");
  //   final response = await http.get(url);

  //   if (response.statusCode == 200) {
  //     final data = json.decode(response.body);
  //     return List<String>.from(data["messages"].map((msg) => msg["message"]));
  //   } else {
  //     throw Exception("Failed to fetch messages");
  //   }
  // }
  Future<List<String>> consumeMessages() async {
  final url = Uri.parse("$baseUrl/consume");
  final response = await http.get(url);

  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    // Extract the "message" field from each item in the "messages" list
    return List<String>.from(data["messages"].map((msg) => msg["message"]));
  } else {
    throw Exception("Failed to fetch messages");
  }
}

}
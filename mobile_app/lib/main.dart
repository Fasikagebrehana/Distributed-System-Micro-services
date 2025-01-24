import 'package:flutter/material.dart';
import 'api_services.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Taskify Mobile App',
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final ApiService apiService = ApiService();
  final TextEditingController routingKeyController = TextEditingController();
  final TextEditingController messageController = TextEditingController();
  List<String> consumedMessages = [];

  void publishMessage() async {
    try {
      await apiService.publishMessage(
        routingKeyController.text,
        messageController.text,
      );
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Message published successfully")),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Failed to publish message: $e")),
      );
    }
  }

  // void fetchMessages() async {
  //   try {
  //     final messages = await apiService.consumeMessages();
  //     setState(() {
  //       consumedMessages = messages;
  //     });
  //     ScaffoldMessenger.of(context).showSnackBar(
  //       SnackBar(content: Text("Messages fetched successfully")),
  //     );
  //   } catch (e) {
  //     ScaffoldMessenger.of(context).showSnackBar(
  //       SnackBar(content: Text("Failed to fetch messages: $e")),
  //     );
  //   }
  // }
  void fetchMessages() async {
  try {
    final messages = await apiService.consumeMessages();
    print("Fetched Messages: $messages"); // Debug log
    setState(() {
      consumedMessages = messages;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("Messages fetched successfully")),
    );
  } catch (e) {
    print("Error fetching messages: $e");
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("Failed to fetch messages: $e")),
    );
  }
}


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Taskify Mobile App'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: routingKeyController,
              decoration: InputDecoration(labelText: 'Routing Key'),
            ),
            TextField(
              controller: messageController,
              decoration: InputDecoration(labelText: 'Message'),
            ),
            SizedBox(height: 16),
            Row(
              children: [
                ElevatedButton(
                  onPressed: publishMessage,
                  child: Text('Publish'),
                ),
                SizedBox(width: 16),
                ElevatedButton(
                  onPressed: fetchMessages,
                  child: Text('Fetch Messages'),
                ),
              ],
            ),
            SizedBox(height: 24),
            Text(
              'Consumed Messages:',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: consumedMessages.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    title: Text(consumedMessages[index]),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  TextEditingController _ctrl = TextEditingController();
  String result = '';

  Future<void> callApi() async{
    final res = await http.post(Uri.parse('http://10.0.2.2:8000/v1/generate'),
      headers: {'Content-Type':'application/json'},
      body: json.encode({'text': _ctrl.text, 'lang':'ar'})
    );
    final data = json.decode(res.body);
    setState(()=> result = data['result']);
  }

  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(title: Text('MindLink')),
      body: Padding(
        padding: EdgeInsets.all(12),
        child: Column(
          children: [
            TextField(controller: _ctrl, maxLines:4),
            ElevatedButton(onPressed: callApi, child: Text('تحويل')),
            SizedBox(height:20),
            Text(result)
          ],
        ),
      ),
    );
  }
}

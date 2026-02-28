import 'package:english_words/english_words.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
void main() {
  runApp(MyApp());
}
class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override 
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => MyAppState(),
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
      title: 'first_application_villaruel',
      theme: ThemeData(
      colorScheme: ColorScheme.fromSeed(seedColor: const Color.fromARGB(255, 239, 177, 207)),
      ),
      home: MyHomePage(),
      ),
      );
    }

  }
  class MyAppState extends ChangeNotifier {
    var current = WordPair.random();
    void getNext(){
      current = WordPair.random();
      notifyListeners();
    }
  }
  class MyHomePage extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
      var appState = context.watch<MyAppState>();
      
      return Scaffold(
        body: Column(
          children: [
            Text('A random idea:'), 
            BigCard(appState: appState),
            ElevatedButton(
              onPressed:() {
                appState.getNext();
              },
              child: Text('Next'),
          ),
        ],
      ),
    );
  }
}

class BigCard extends StatelessWidget {
  const BigCard({
    super.key,
    required this.appState,
  });

  final MyAppState appState;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final style = theme.textTheme.displayMedium!.copyWith(
      color: theme.colorScheme.onPrimary,
    );
    return Card(
      color: theme.colorScheme.primary,
      child: Padding(
        padding: const EdgeInsets.all(10),
        child: Text(appState.current.asLowerCase),
      ),
    );
  }
} 
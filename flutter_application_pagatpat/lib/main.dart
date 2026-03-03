import 'dart:convert';

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const EmoTuneApp());
}

class EmoTuneApp extends StatefulWidget {
  const EmoTuneApp({super.key});

  @override
  State<EmoTuneApp> createState() => _EmoTuneAppState();
}

class _EmoTuneAppState extends State<EmoTuneApp> {
  bool darkMode = true;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EmoTune',
      debugShowCheckedModeBanner: false,
      themeMode: darkMode ? ThemeMode.dark : ThemeMode.light,
      darkTheme: ThemeData.dark(useMaterial3: true).copyWith(
        colorScheme: const ColorScheme.dark(primary: Color(0xFFA8E95D)),
      ),
      theme: ThemeData.light(useMaterial3: true).copyWith(
        colorScheme: const ColorScheme.light(primary: Color(0xFFA8E95D)),
      ),
      home: IntroScreen(
        onContinue: () => Navigator.of(context).pushReplacement(
          MaterialPageRoute(
            builder: (_) => AuthScreen(
              onLogin: () => Navigator.of(context).pushReplacement(
                MaterialPageRoute(
                  builder: (_) => HomeShell(
                    darkMode: darkMode,
                    onThemeChanged: (v) => setState(() => darkMode = v),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class IntroScreen extends StatelessWidget {
  final VoidCallback onContinue;
  const IntroScreen({super.key, required this.onContinue});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.black,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const CircleAvatar(radius: 60, backgroundColor: Color(0xFF58DBF4), child: Icon(Icons.graphic_eq, size: 50)),
              const SizedBox(height: 12),
              Text('EmoTune', style: Theme.of(context).textTheme.headlineMedium?.copyWith(color: const Color(0xFFA8E95D), fontWeight: FontWeight.bold)),
              const SizedBox(height: 50),
              SizedBox(
                width: 220,
                child: FilledButton(
                  style: FilledButton.styleFrom(backgroundColor: const Color(0xFFA8E95D), foregroundColor: Colors.black),
                  onPressed: onContinue,
                  child: const Text('Get Started'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class AuthScreen extends StatefulWidget {
  final VoidCallback onLogin;
  const AuthScreen({super.key, required this.onLogin});

  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  bool register = false;
  final username = TextEditingController();
  final email = TextEditingController();
  final password = TextEditingController();
  final api = ApiService();

  Future<void> submit() async {
    final ok = await api.register(username.text.trim(), email.text.trim(), password.text.trim());
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(ok ? 'Account ready. Signed in via Spotify flow placeholder.' : 'Unable to register now')),
    );
    if (ok) widget.onLogin();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SizedBox(
          width: 360,
          child: Card(
            color: const Color(0xFF151515),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(mainAxisSize: MainAxisSize.min, children: [
                Text('EmoTune', style: Theme.of(context).textTheme.headlineMedium?.copyWith(color: const Color(0xFFA8E95D))),
                const SizedBox(height: 12),
                Text(register ? 'Create account' : 'Proceed with your login'),
                const SizedBox(height: 16),
                TextField(controller: username, decoration: const InputDecoration(labelText: 'Username')),
                if (register) TextField(controller: email, decoration: const InputDecoration(labelText: 'Email')),
                TextField(controller: password, obscureText: true, decoration: const InputDecoration(labelText: 'Password')),
                const SizedBox(height: 20),
                FilledButton(
                  style: FilledButton.styleFrom(backgroundColor: const Color(0xFFA8E95D), foregroundColor: Colors.black),
                  onPressed: submit,
                  child: Text(register ? 'Create & Login with Spotify' : 'Login with Spotify'),
                ),
                TextButton(onPressed: () => setState(() => register = !register), child: Text(register ? 'Already have an account?' : 'Create an account')),
              ]),
            ),
          ),
        ),
      ),
    );
  }
}

class HomeShell extends StatefulWidget {
  final bool darkMode;
  final ValueChanged<bool> onThemeChanged;
  const HomeShell({super.key, required this.darkMode, required this.onThemeChanged});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  int index = 0;
  final appState = EmoTuneState();

  @override
  Widget build(BuildContext context) {
    final pages = [
      HomePage(state: appState),
      FavoritesPage(state: appState),
      RecommendationPage(state: appState),
      HistoryPage(state: appState),
      ProfilePage(state: appState, darkMode: widget.darkMode, onThemeChanged: widget.onThemeChanged),
    ];

    return Scaffold(
      body: pages[index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (i) => setState(() => index = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.favorite_border), label: 'Favorite'),
          NavigationDestination(icon: Icon(Icons.auto_awesome), label: 'Recommendation'),
          NavigationDestination(icon: Icon(Icons.history), label: 'History'),
          NavigationDestination(icon: Icon(Icons.person_outline), label: 'Profile'),
        ],
      ),
    );
  }
}

class EmoTuneState {
  final ApiService api = ApiService();
  List<dynamic> tracks = [];
  List<dynamic> favorites = [];
  List<dynamic> history = [];
  Map<String, int> emotionCount = {};
  String emotion = 'Mixed';
  String aiMessage = 'Tell me how you feel and I will recommend music for your mood.';
  final AudioPlayer player = AudioPlayer();

  Future<void> prompt(String text, {String artist = ''}) async {
    final response = await api.promptMood(text, artist: artist);
    emotion = response['emotion'] ?? 'Mixed';
    aiMessage = response['ai_message'] ?? aiMessage;
    tracks = response['tracks'] ?? [];
    emotionCount[emotion] = (emotionCount[emotion] ?? 0) + 1;
    await loadHistory();
  }

  Future<void> loadFavorites() async {
    favorites = await api.favorites();
  }

  Future<void> loadHistory() async {
    history = await api.history();
  }

  Future<void> addFavorite(Map<String, dynamic> track) async {
    await api.addFavorite(track);
    await loadFavorites();
  }
}

class HomePage extends StatefulWidget {
  final EmoTuneState state;
  const HomePage({super.key, required this.state});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final promptController = TextEditingController();
  final artistController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: ListView(children: [
        Text('Welcome to EmoTune', style: Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height: 8),
        Text(widget.state.aiMessage),
        const SizedBox(height: 12),
        TextField(controller: artistController, decoration: const InputDecoration(labelText: 'Select artist preference')),
        TextField(controller: promptController, decoration: const InputDecoration(labelText: 'I feel...')),
        const SizedBox(height: 8),
        FilledButton(
          onPressed: () async {
            await widget.state.prompt(promptController.text, artist: artistController.text);
            if (!mounted) return;
            setState(() {});
          },
          child: const Text('Recommend playlist'),
        ),
        const SizedBox(height: 10),
        Text('Detected emotion: ${widget.state.emotion}'),
        const SizedBox(height: 10),
        ...widget.state.tracks.map((t) => Card(
              child: ListTile(
                title: Text(t['name'] ?? 'Unknown track'),
                subtitle: Text(t['artist'] ?? ''),
                trailing: Wrap(spacing: 10, children: [
                  IconButton(
                    icon: const Icon(Icons.play_arrow),
                    onPressed: () async {
                      if ((t['preview_url'] ?? '').toString().isNotEmpty) {
                        await widget.state.player.play(UrlSource(t['preview_url']));
                      }
                    },
                  ),
                  IconButton(icon: const Icon(Icons.pause), onPressed: () => widget.state.player.pause()),
                  IconButton(
                    icon: const Icon(Icons.favorite_border),
                    onPressed: () async {
                      await widget.state.addFavorite(Map<String, dynamic>.from(t));
                      if (!mounted) return;
                      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Added to favorites')));
                    },
                  ),
                ]),
              ),
            )),
      ]),
    );
  }
}

class FavoritesPage extends StatefulWidget {
  final EmoTuneState state;
  const FavoritesPage({super.key, required this.state});

  @override
  State<FavoritesPage> createState() => _FavoritesPageState();
}

class _FavoritesPageState extends State<FavoritesPage> {
  @override
  void initState() {
    super.initState();
    widget.state.loadFavorites().then((_) => setState(() {}));
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text('Favorites', style: Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height: 8),
        ...widget.state.favorites.map((f) => ListTile(title: Text(f['track_name'] ?? ''), subtitle: Text(f['artist'] ?? ''))),
      ],
    );
  }
}

class RecommendationPage extends StatelessWidget {
  final EmoTuneState state;
  const RecommendationPage({super.key, required this.state});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text('Adaptive Recommendations', style: Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height: 8),
        const Text('The backend prioritizes repeatedly played tracks for the same emotion and can ask "Feel better?" after long listening sessions.'),
      ],
    );
  }
}

class HistoryPage extends StatefulWidget {
  final EmoTuneState state;
  const HistoryPage({super.key, required this.state});

  @override
  State<HistoryPage> createState() => _HistoryPageState();
}

class _HistoryPageState extends State<HistoryPage> {
  @override
  void initState() {
    super.initState();
    widget.state.loadHistory().then((_) => setState(() {}));
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text('History', style: Theme.of(context).textTheme.headlineSmall),
        ...widget.state.history.map((h) => ListTile(title: Text(h['text'] ?? ''), subtitle: Text(h['emotion'] ?? ''))),
      ],
    );
  }
}

class ProfilePage extends StatelessWidget {
  final EmoTuneState state;
  final bool darkMode;
  final ValueChanged<bool> onThemeChanged;
  const ProfilePage({super.key, required this.state, required this.darkMode, required this.onThemeChanged});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text('Profile', style: Theme.of(context).textTheme.headlineSmall),
        const SizedBox(height: 8),
        SwitchListTile(
          title: const Text('Night mode'),
          value: darkMode,
          onChanged: onThemeChanged,
        ),
        const SizedBox(height: 8),
        Text('Mood prompt distribution (pie-like summary):', style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: 6),
        ...state.emotionCount.entries.map((e) => ListTile(title: Text(e.key), trailing: Text('${e.value}'))),
      ],
    );
  }
}

class ApiService {
  static const String baseUrl = String.fromEnvironment('API_URL', defaultValue: 'http://127.0.0.1:8000/api');
  final int userId = 1;

  Future<bool> register(String username, String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username.isEmpty ? 'demo' : username, 'email': email, 'password': password.isEmpty ? 'demo12345' : password}),
    );
    return response.statusCode < 300;
  }

  Future<Map<String, dynamic>> promptMood(String text, {String artist = ''}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/mood/prompt/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'user_id': userId, 'text': text, 'selected_artist': artist}),
    );
    if (response.statusCode >= 300) return {};
    return jsonDecode(response.body);
  }

  Future<void> addFavorite(Map<String, dynamic> track) async {
    await http.post(
      Uri.parse('$baseUrl/favorites/add/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'user': userId,
        'spotify_track_id': track['id'] ?? '',
        'track_name': track['name'] ?? '',
        'artist': track['artist'] ?? '',
        'image_url': track['image_url'] ?? '',
        'preview_url': track['preview_url'] ?? '',
      }),
    );
  }

  Future<List<dynamic>> favorites() async {
    final response = await http.get(Uri.parse('$baseUrl/favorites/$userId/'));
    if (response.statusCode >= 300) return [];
    return jsonDecode(response.body);
  }

  Future<List<dynamic>> history() async {
    final response = await http.get(Uri.parse('$baseUrl/history/$userId/'));
    if (response.statusCode >= 300) return [];
    return jsonDecode(response.body);
  }
}

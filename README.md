# MLEngagementTool
## Description
This repo is to develop the Windows desktop application for the project "Measuring Student Engagement using Machine Learning". 
- Framework: WPF ([.NET 7.0](https://dotnet.microsoft.com/en-us/download/dotnet/7.0))
- Pattern: Model-View-ViewModel (MVVM)
- Programming Language: C# and XAML

## How to Run
```bash
dotnet run
```

## Directory Structure

*For reference only*

```
MLEngagementTool/
│
├── Properties/               # Project properties
│
├── Views/                    # WPF views
│   ├── VideoRecordingView.xaml   # WPF interface for video recording
│   ├── ParticipationAnalysisView.xaml  # WPF interface for participation analysis
│   ├── QuizView.xaml           # WPF interface for the quiz
│
├── ViewModels/               # WPF view models (Intermediary between view and model)
│   ├── VideoRecordingViewModel.cs  # View model for video recording
│   ├── ParticipationAnalysisViewModel.cs  # View model for participation analysis
│   ├── QuizViewModel.cs           # View model for the quiz
│
├── Models/                   # Data models
│   ├── VideoModel.cs         # Data model for video
│   ├── AnalysisModel.cs      # Data model for participation analysis
│   ├── QuizModel.cs          # Data model for the quiz
│
├── Services/                 # Services and business logic
│   ├── VideoRecordingService.cs  # Video recording service
│   ├── AnalysisService.cs       # Participation analysis service
│   ├── QuizService.cs           # Quiz service
│
├── Utils/                    # Utility classes (Functions for general tasks)
│   ├── FileHelper.cs         # File operations helper
│
├── Resources/                # Resource files (images, audio, etc.)
│
├── App.config                # Project configuration file
│
├── App.xaml                  # Main application XAML file
│
├── App.xaml.cs               # Main application code file
│
├── MainWindow.xaml           # Main window XAML file
│
├── MainWindow.xaml.cs        # Main window code file
│
├── Packages/                 # NuGet packages (if used)
│
├── bin/                       # Output directory
│
├── obj/                       # Temporary build files
│
└── README.md                 # Project documentation
```

## Tutorial

Steps:

1. Clone the [wpf tutorial](https://github.com/SingletonSean/wpf-tutorials/tree/master) repo from GitHub
2. To run the code examples, download the particular version of .NET required for the specific code example. The required version can be found in the `/obj/project.assets.json` file
    - [.NET Core 3.1](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/sdk-3.1.426-windows-x64-installer)
        - This version covers most code examples
    - [.NET 5.0 SDK](https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/sdk-5.0.408-windows-x64-installer)
        - Required for `AnimationDemo`,  `BindingShort`, `CommunicationMVVM`, `ConditionalRendering`, `ItemsControlDemo`, `NavigationMVVMEssentialsDemo`,  `WPFMVVMTemplate`
    - .NET 6.0
        - Required for  `DashboardMVVM`, `EffectiveValidation`
2.  Navigate to the subfolder of the specific code example and run `dotnet run` to check it out

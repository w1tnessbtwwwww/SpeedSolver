using Avalonia;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using DesktopApp.DTO;
using MsBox.Avalonia;
using MsBox.Avalonia.Enums;
using DesktopApp.APIService;
namespace DesktopApp.Views.UC;

public partial class RegisterWindow : UserControl
{

    private MainWindow _parent;
    public RegisterWindow(MainWindow parent)
    {
        InitializeComponent();
        _parent = parent;
    }

    private async void RegisterBtn_OnClick(object? sender, RoutedEventArgs e)
    {
        if (RepeatPasswordBox.Text != PasswordBox.Text)
        {
            MessageBoxManager.GetMessageBoxStandard("Ошибка", "Пароли не совпадают.", ButtonEnum.Ok).ShowAsync();
            return;
        }

        var build = RegisterRequest.Create(LoginBox.Text, PasswordBox.Text);
        if (build.IsFailure)
        {
            MessageBoxManager.GetMessageBoxStandard("Ошибка", build.Error).ShowAsync();
            return;
        }

        var service = APIService.APIService
            .BuildService()
            .WithUrl();

        var register = await service.RegisterUser(build.Value);
            

        if (register.IsFailure)
        {
            await MessageBoxManager.GetMessageBoxStandard("Error", register.Error).ShowAsync();
            return;
        }

        MessageBoxManager.GetMessageBoxStandard("Успешно", "Вы зарегистрировались в сервисе.").ShowAsync();
        this._parent.UserActionControl.Content = new AuthozationWindow(_parent);
    }
}
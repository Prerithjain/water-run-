import { Droplets, Moon, Sun, Gamepad2 } from 'lucide-react';
import { useTheme } from 'next-themes';
import { useState, useEffect } from 'react';
import FlappyGame from './FlappyGame';

export default function Header() {
    const { theme, setTheme, resolvedTheme } = useTheme();
    const [mounted, setMounted] = useState(false);
    const [showGame, setShowGame] = useState(false);

    useEffect(() => setMounted(true), []);

    return (
        <>
            <header className="flex flex-col md:flex-row md:items-center justify-between py-6 mb-8 gap-4">
                <div className="flex items-center gap-3">
                    <div className="bg-blue-500 p-2 rounded-xl shadow-lg shadow-blue-500/30">
                        <Droplets className="text-white w-6 h-6" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold text-slate-800 dark:text-white tracking-tight">Water Run</h1>
                        <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">Fairness Tracker</p>
                    </div>
                </div>
                <div className="flex items-center gap-3 self-end md:self-auto">
                    <button
                        onClick={() => setShowGame(true)}
                        className="p-2 rounded-lg bg-indigo-100 text-indigo-600 dark:bg-indigo-900/30 dark:text-indigo-400 hover:bg-indigo-200 dark:hover:bg-indigo-900/50 transition-colors"
                        title="Play Game"
                    >
                        <Gamepad2 size={20} />
                    </button>
                    <button
                        onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
                        className="p-2 rounded-lg bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
                    >
                        {mounted && resolvedTheme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
                    </button>
                    <div className="text-right border-l pl-4 border-slate-200 dark:border-slate-700">
                        <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">
                            {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })}
                        </p>
                    </div>
                </div>
            </header>
            {showGame && <FlappyGame onClose={() => setShowGame(false)} />}
        </>
    );
}

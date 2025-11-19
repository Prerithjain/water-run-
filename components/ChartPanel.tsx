'use client';
import { Person } from '@/app/types';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

export default function ChartPanel({ people }: { people: Person[] }) {
    const data = {
        labels: people.map(p => p.name),
        datasets: [
            {
                label: 'Points',
                data: people.map(p => p.score),
                backgroundColor: 'rgba(99, 102, 241, 0.8)', // Indigo 500
                hoverBackgroundColor: 'rgba(99, 102, 241, 1)',
                borderRadius: 6,
                borderSkipped: false,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: false,
            },
            tooltip: {
                backgroundColor: 'rgba(17, 24, 39, 0.9)',
                padding: 12,
                cornerRadius: 12,
                titleFont: {
                    size: 14,
                    family: "'Inter', sans-serif",
                },
                bodyFont: {
                    size: 13,
                    family: "'Inter', sans-serif",
                },
                displayColors: false,
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(148, 163, 184, 0.1)',
                    drawBorder: false,
                },
                ticks: {
                    font: {
                        family: "'Inter', sans-serif",
                    },
                    color: '#94a3b8'
                },
                border: {
                    display: false
                }
            },
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    font: {
                        family: "'Inter', sans-serif",
                        weight: 'bold'
                    },
                    color: '#64748b'
                },
                border: {
                    display: false
                }
            },
        },
        animation: {
            duration: 750,
            easing: 'easeOutQuart' as const,
        }
    };

    return (
        <div className="bg-white/60 dark:bg-slate-900/60 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/50 dark:border-slate-800 h-full flex flex-col">
            <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-200 mb-4">Scoreboard</h3>
            <div className="flex-1 min-h-[200px]">
                <Bar data={data} options={options} />
            </div>
        </div>
    );
}

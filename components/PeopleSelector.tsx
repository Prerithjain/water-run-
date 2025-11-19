import { Person } from '@/app/types';
import { Check } from 'lucide-react';
import { clsx } from 'clsx';

interface Props {
    people: Person[];
    selectedIds: number[];
    onToggle: (id: number) => void;
}

export default function PeopleSelector({ people, selectedIds, onToggle }: Props) {
    return (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 md:gap-4">
            {people.map((p) => {
                const isSelected = selectedIds.includes(p.id);
                return (
                    <button
                        key={p.id}
                        onClick={() => onToggle(p.id)}
                        className={clsx(
                            "relative p-3 md:p-4 rounded-2xl transition-all duration-300 border flex flex-col items-center justify-center gap-2 shadow-sm hover:shadow-md touch-manipulation",
                            isSelected
                                ? "bg-indigo-600 text-white border-indigo-500 scale-[1.02] ring-2 md:ring-4 ring-indigo-500/20"
                                : "bg-white/60 dark:bg-slate-900/60 backdrop-blur-md text-slate-700 dark:text-slate-200 border-white/50 dark:border-slate-800 hover:bg-white dark:hover:bg-slate-900 hover:scale-[1.02]"
                        )}
                    >
                        {isSelected && (
                            <div className="absolute top-2 right-2 bg-white/20 rounded-full p-1">
                                <Check size={12} className="text-white" />
                            </div>
                        )}
                        <div className={clsx(
                            "w-10 h-10 md:w-12 md:h-12 rounded-full flex items-center justify-center text-lg md:text-xl font-bold mb-1 transition-colors shrink-0",
                            isSelected ? "bg-white/20" : "bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400"
                        )}>
                            {p.name.charAt(0)}
                        </div>
                        <span className="font-semibold text-sm md:text-lg text-center leading-tight break-words w-full px-1">
                            {p.name}
                        </span>
                        <div className="text-xs opacity-80 flex flex-col items-center gap-0.5">
                            <span className="font-medium">{p.score} pts</span>
                            <span className="text-[10px] opacity-70">
                                {p.last_visit ? new Date(p.last_visit).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) : 'Never'}
                            </span>
                        </div>
                    </button>
                );
            })}
        </div>
    );
}

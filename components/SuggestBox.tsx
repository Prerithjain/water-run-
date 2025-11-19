import { SuggestionResponse } from '@/app/types';
import { Sparkles } from 'lucide-react';

interface Props {
    suggestion: SuggestionResponse | null;
}

export default function SuggestBox({ suggestion }: Props) {
    if (!suggestion || suggestion.suggested.length === 0) return null;

    return (
        <div className="bg-gradient-to-br from-violet-600 to-indigo-600 p-6 rounded-2xl text-white shadow-xl shadow-indigo-500/20 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full -mr-10 -mt-10 blur-3xl"></div>
            <div className="absolute bottom-0 left-0 w-32 h-32 bg-fuchsia-500/20 rounded-full -ml-10 -mb-10 blur-2xl"></div>

            <div className="relative z-10">
                <div className="flex items-center gap-2 mb-3 text-indigo-100">
                    <Sparkles size={16} />
                    <span className="text-xs font-bold uppercase tracking-widest">Smart Suggestion</span>
                </div>

                <div className="flex items-center gap-4 mb-5">
                    <div className="flex -space-x-3">
                        {suggestion.suggested.map((p) => (
                            <div key={p.id} className="w-14 h-14 rounded-full bg-white text-indigo-600 flex items-center justify-center font-bold text-xl border-4 border-indigo-500/30 shadow-lg">
                                {p.name.charAt(0)}
                            </div>
                        ))}
                    </div>
                    <div className="flex flex-col">
                        <span className="text-2xl font-bold leading-none">
                            {suggestion.suggested.map(p => p.name).join(' & ')}
                        </span>
                        <span className="text-indigo-200 text-sm mt-1">Should go next</span>
                    </div>
                </div>

                <div className="bg-white/10 rounded-lg p-3 backdrop-blur-sm border border-white/10">
                    <p className="text-indigo-50 text-xs leading-relaxed">
                        <span className="font-semibold text-white">Why?</span> {suggestion.reason}
                    </p>
                </div>
            </div>
        </div>
    );
}

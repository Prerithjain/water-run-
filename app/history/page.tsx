'use client';
import useSWR from 'swr';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { Run } from '@/app/types';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function HistoryPage() {
    const { data: history } = useSWR<Run[]>('/api/history?limit=100', fetcher);

    return (
        <main className="min-h-screen bg-slate-50 p-4 md:p-8 font-sans text-slate-900">
            <div className="max-w-4xl mx-auto">
                <div className="mb-8">
                    <Link href="/" className="inline-flex items-center gap-2 text-slate-500 hover:text-slate-800 transition-colors mb-4">
                        <ArrowLeft size={16} />
                        Back to Dashboard
                    </Link>
                    <h1 className="text-2xl font-bold text-slate-800">Run History</h1>
                </div>

                <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-slate-50 border-b border-slate-200">
                                <tr>
                                    <th className="px-6 py-4 font-semibold text-slate-700">Date</th>
                                    <th className="px-6 py-4 font-semibold text-slate-700">Mode</th>
                                    <th className="px-6 py-4 font-semibold text-slate-700">People</th>
                                    <th className="px-6 py-4 font-semibold text-slate-700 text-right">Points</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {!history ? (
                                    <tr><td colSpan={4} className="px-6 py-8 text-center text-slate-500">Loading...</td></tr>
                                ) : history.length === 0 ? (
                                    <tr><td colSpan={4} className="px-6 py-8 text-center text-slate-500">No runs recorded yet.</td></tr>
                                ) : (
                                    history.map((run) => (
                                        <tr key={run.id} className="hover:bg-slate-50/50 transition-colors">
                                            <td className="px-6 py-4 text-slate-600">
                                                {new Date(run.timestamp).toLocaleString()}
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${run.mode === 'alone' ? 'bg-blue-100 text-blue-800' : 'bg-indigo-100 text-indigo-800'
                                                    }`}>
                                                    {run.mode === 'alone' ? 'Solo' : 'Group'}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-slate-800 font-medium">
                                                {run.actor_names.join(', ')}
                                            </td>
                                            <td className="px-6 py-4 text-right text-slate-600">
                                                +{run.points_each} ea
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </main>
    );
}

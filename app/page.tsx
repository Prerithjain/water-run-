'use client';

import { useState, useEffect } from 'react';
import useSWR, { mutate } from 'swr';
import Header from '@/components/Header';
import PeopleSelector from '@/components/PeopleSelector';
import ChartPanel from '@/components/ChartPanel';
import SuggestBox from '@/components/SuggestBox';
import { StateResponse, SuggestionResponse } from './types';
import Link from 'next/link';
import { History, Download, FileText, Users, User } from 'lucide-react';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function Home() {
  const { data: state, error: stateError } = useSWR<StateResponse>('/api/state', fetcher);
  const { data: suggestion, error: suggestError } = useSWR<SuggestionResponse>('/api/suggest', fetcher);

  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [isRecording, setIsRecording] = useState(false);
  const [message, setMessage] = useState<{ text: string, type: 'success' | 'error' } | null>(null);

  const [isAdmin, setIsAdmin] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [password, setPassword] = useState('');

  // Check admin status on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('water_admin');
      if (stored === 'true') setIsAdmin(true);
    }
  }, []);

  const handleLogin = () => {
    if (password === 'water123') { // Simple hardcoded password
      setIsAdmin(true);
      localStorage.setItem('water_admin', 'true');
      setShowLogin(false);
      setMessage({ text: 'Admin access granted', type: 'success' });
    } else {
      setMessage({ text: 'Incorrect password', type: 'error' });
    }
  };

  const handleLogout = () => {
    setIsAdmin(false);
    localStorage.removeItem('water_admin');
    setMessage({ text: 'Logged out', type: 'success' });
  };

  const togglePerson = (id: number) => {
    setSelectedIds(prev =>
      prev.includes(id) ? prev.filter(p => p !== id) : [...prev, id]
    );
  };

  const recordRun = async (mode: 'alone' | 'group', actors: number[]) => {
    if (!isAdmin) return;
    setIsRecording(true);
    setMessage(null);
    try {
      const res = await fetch('/api/record', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode, actors })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to record');
      }

      // Success
      setMessage({ text: 'Run recorded successfully!', type: 'success' });
      setSelectedIds([]);
      mutate('/api/state');
      mutate('/api/suggest');
      mutate('/api/history');
    } catch (e: any) {
      setMessage({ text: e.message, type: 'error' });
    } finally {
      setIsRecording(false);
      setTimeout(() => setMessage(null), 3000);
    }
  };

  const handleGoAlone = () => {
    if (selectedIds.length !== 1) {
      setMessage({ text: 'Please select exactly one person for "Go Alone"', type: 'error' });
      return;
    }
    recordRun('alone', selectedIds);
  };

  const handleGoGroup = () => {
    if (selectedIds.length < 2) {
      setMessage({ text: 'Please select at least two people for "Go Together"', type: 'error' });
      return;
    }
    recordRun('group', selectedIds);
  };

  const handleAcceptSuggestion = () => {
    if (!suggestion) return;
    recordRun('group', suggestion.suggested.map(p => p.id));
  };

  const exportPDF = async () => {
    const doc = new jsPDF();
    doc.setFontSize(20);
    doc.text("Water Run Report", 14, 22);
    doc.setFontSize(11);
    doc.text(`Generated on ${new Date().toLocaleDateString()}`, 14, 30);

    if (state) {
      const stats = state.people.map(p => [p.name, p.score, p.last_visit ? new Date(p.last_visit).toLocaleDateString() : 'Never']);
      autoTable(doc, {
        head: [['Name', 'Score', 'Last Visit']],
        body: stats,
        startY: 40,
      });
    }

    doc.save("water-run-report.pdf");
  };

  if (!state) return <div className="min-h-screen flex items-center justify-center text-slate-500">Loading...</div>;

  return (
    <main className="min-h-screen bg-slate-50 dark:bg-slate-950 p-3 md:p-8 font-sans text-slate-900 dark:text-slate-100">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-start">
          <Header />
          <button
            onClick={() => isAdmin ? handleLogout() : setShowLogin(!showLogin)}
            className="text-xs text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 mt-6"
          >
            {isAdmin ? 'Logout' : 'Admin'}
          </button>
        </div>

        {showLogin && !isAdmin && (
          <div className="mb-6 p-4 bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 animate-in slide-in-from-top-2">
            <p className="text-sm font-bold text-slate-700 dark:text-slate-200 mb-2">Admin Access</p>
            <div className="flex gap-2">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                className="flex-1 px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-slate-800 dark:border-slate-700 dark:text-white"
              />
              <button
                onClick={handleLogin}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-bold hover:bg-indigo-700"
              >
                Unlock
              </button>
            </div>
          </div>
        )}

        {message && (
          <div className={`fixed top-4 right-4 left-4 md:left-auto p-4 rounded-xl shadow-lg z-50 text-white font-medium animate-in slide-in-from-top-2 ${message.type === 'success' ? 'bg-emerald-500' : 'bg-rose-500'}`}>
            {message.text}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
          <div className="lg:col-span-2 space-y-6 md:space-y-8">
            <section>
              <h2 className="text-lg md:text-xl font-bold text-slate-800 dark:text-slate-100 mb-3 md:mb-4">Who is going?</h2>
              <PeopleSelector
                people={state.people}
                selectedIds={selectedIds}
                onToggle={togglePerson}
              />
            </section>

            {isAdmin ? (
              <section className="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                <button
                  onClick={handleGoAlone}
                  disabled={isRecording}
                  className="group relative overflow-hidden bg-white dark:bg-slate-900 p-5 md:p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all text-left touch-manipulation active:scale-[0.98]"
                >
                  <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                    <User size={48} className="text-blue-500" />
                  </div>
                  <span className="block text-lg font-bold text-slate-800 dark:text-slate-100 mb-1">Go Alone</span>
                  <span className="text-sm text-slate-500 dark:text-slate-400">2 points per person</span>
                </button>

                <button
                  onClick={handleGoGroup}
                  disabled={isRecording}
                  className="group relative overflow-hidden bg-white dark:bg-slate-900 p-5 md:p-6 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all text-left touch-manipulation active:scale-[0.98]"
                >
                  <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                    <Users size={48} className="text-indigo-500" />
                  </div>
                  <span className="block text-lg font-bold text-slate-800 dark:text-slate-100 mb-1">Go Together</span>
                  <span className="text-sm text-slate-500 dark:text-slate-400">1 point per person</span>
                </button>
              </section>
            ) : (
              <div className="p-6 bg-slate-100 dark:bg-slate-900 rounded-2xl text-center text-slate-500 dark:text-slate-400 text-sm">
                Admin access required to record runs.
              </div>
            )}

            <section className="flex gap-3 flex-wrap">
              <Link href="/history" className="flex-1 sm:flex-none justify-center flex items-center gap-2 px-4 py-3 bg-white dark:bg-slate-900 rounded-xl text-sm font-medium text-slate-600 dark:text-slate-300 border dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors touch-manipulation">
                <History size={16} />
                History
              </Link>
              <a href="/api/export/csv" className="flex-1 sm:flex-none justify-center flex items-center gap-2 px-4 py-3 bg-white dark:bg-slate-900 rounded-xl text-sm font-medium text-slate-600 dark:text-slate-300 border dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors touch-manipulation">
                <FileText size={16} />
                CSV
              </a>
              <button onClick={exportPDF} className="flex-1 sm:flex-none justify-center flex items-center gap-2 px-4 py-3 bg-white dark:bg-slate-900 rounded-xl text-sm font-medium text-slate-600 dark:text-slate-300 border dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors touch-manipulation">
                <Download size={16} />
                PDF
              </button>
            </section>
          </div>

          <div className="space-y-6">
            <SuggestBox
              suggestion={suggestion || null}
            />
            <div className="h-64 lg:h-auto">
              <ChartPanel people={state.people} />
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

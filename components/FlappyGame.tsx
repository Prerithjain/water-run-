"use client";

import { useEffect, useRef, useState } from "react";
import { X, Play, RotateCcw } from "lucide-react";

interface FlappyGameProps {
    onClose: () => void;
}

export default function FlappyGame({ onClose }: FlappyGameProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [score, setScore] = useState(0);
    const [gameOver, setGameOver] = useState(false);
    const [won, setWon] = useState(false);

    // Game constants
    const GRAVITY = 0.6;
    const JUMP = -10;
    const PIPE_SPEED = 3;
    const PIPE_SPAWN_RATE = 100; // frames
    const GAP_SIZE = 150;

    const gameState = useRef({
        birdY: 200,
        birdVelocity: 0,
        pipes: [] as { x: number; topHeight: number; passed: boolean }[],
        frameCount: 0,
        animationId: 0
    });

    const playAudio = (type: 'lose' | 'win') => {
        // Try to play audio if it exists
        try {
            const audio = new Audio(type === 'lose' ? '/audio/lose.mp3' : '/audio/win.mp3');
            audio.play().catch(e => console.log("Audio play failed", e));
        } catch (e) {
            console.log("Audio not supported");
        }
    };

    const startGame = () => {
        cancelAnimationFrame(gameState.current.animationId);
        setIsPlaying(true);
        setGameOver(false);
        setWon(false);
        setScore(0);
        gameState.current = {
            birdY: 200,
            birdVelocity: 0,
            pipes: [],
            frameCount: 0,
            animationId: 0
        };
        loop();
    };

    const jump = () => {
        if (!isPlaying || gameOver) return;
        gameState.current.birdVelocity = JUMP;
    };

    const loop = () => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        const state = gameState.current;

        // Update physics
        state.birdVelocity += GRAVITY;
        state.birdY += state.birdVelocity;

        // Spawn pipes
        if (state.frameCount % PIPE_SPAWN_RATE === 0) {
            const minPipe = 50;
            const maxPipe = canvas.height - GAP_SIZE - minPipe;
            const topHeight = Math.floor(Math.random() * (maxPipe - minPipe + 1)) + minPipe;
            state.pipes.push({ x: canvas.width, topHeight, passed: false });
        }

        // Update pipes
        state.pipes.forEach(pipe => {
            pipe.x -= PIPE_SPEED;
        });

        // Remove off-screen pipes
        state.pipes = state.pipes.filter(pipe => pipe.x > -50);

        // Collision detection
        const birdSize = 30;
        const birdX = 50;

        // Floor/Ceiling collision
        if (state.birdY + birdSize > canvas.height || state.birdY < 0) {
            endGame();
            return;
        }

        // Pipe collision
        state.pipes.forEach(pipe => {
            // Check if bird is within pipe's horizontal area
            if (birdX + birdSize > pipe.x && birdX < pipe.x + 50) {
                // Check vertical collision (hit top pipe OR hit bottom pipe)
                if (state.birdY < pipe.topHeight || state.birdY + birdSize > pipe.topHeight + GAP_SIZE) {
                    endGame();
                    return;
                }
            }

            // Score update
            if (!pipe.passed && birdX > pipe.x + 50) {
                pipe.passed = true;
                setScore(prev => {
                    const newScore = prev + 1;
                    if (newScore === 10) { // Win condition
                        setWon(true);
                        // playAudio('win'); // Optional win sound
                    }
                    return newScore;
                });
            }
        });

        if (gameOver) return;

        // Draw
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw Bird (Water Can)
        ctx.font = "30px Arial";
        ctx.fillText("🪣", birdX, state.birdY + 25);

        // Draw Pipes
        ctx.fillStyle = "#22c55e"; // Green pipes
        state.pipes.forEach(pipe => {
            // Top pipe
            ctx.fillRect(pipe.x, 0, 50, pipe.topHeight);
            // Bottom pipe
            ctx.fillRect(pipe.x, pipe.topHeight + GAP_SIZE, 50, canvas.height - (pipe.topHeight + GAP_SIZE));
        });

        state.frameCount++;
        state.animationId = requestAnimationFrame(loop);
    };

    const endGame = () => {
        setGameOver(true);
        setIsPlaying(false);
        cancelAnimationFrame(gameState.current.animationId);
        playAudio('lose');
    };

    useEffect(() => {
        return () => cancelAnimationFrame(gameState.current.animationId);
    }, []);

    return (
        <div className="fixed inset-0 bg-black/80 z-[100] flex items-center justify-center p-4 backdrop-blur-sm">
            <div className="bg-white dark:bg-slate-900 p-4 rounded-2xl shadow-2xl max-w-md w-full relative">
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-slate-500 hover:text-slate-800 dark:hover:text-white"
                >
                    <X size={24} />
                </button>

                <h2 className="text-2xl font-bold text-center mb-4 text-slate-800 dark:text-white">Flappy Can</h2>

                <div className="relative bg-sky-300 dark:bg-sky-900 rounded-xl overflow-hidden cursor-pointer" onClick={jump}>
                    <canvas
                        ref={canvasRef}
                        width={320}
                        height={480}
                        className="w-full h-auto block"
                    />

                    {!isPlaying && !gameOver && !won && (
                        <div className="absolute inset-0 flex items-center justify-center bg-black/20">
                            <button
                                onClick={(e) => { e.stopPropagation(); startGame(); }}
                                className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-full font-bold flex items-center gap-2 transform transition-transform hover:scale-105"
                            >
                                <Play size={20} /> Start Game
                            </button>
                        </div>
                    )}

                    {gameOver && (
                        <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/50 text-white">
                            <p className="text-3xl font-bold mb-2">Game Over</p>
                            <p className="text-xl mb-4">Score: {score}</p>
                            <button
                                onClick={(e) => { e.stopPropagation(); startGame(); }}
                                className="bg-white text-slate-900 px-6 py-3 rounded-full font-bold flex items-center gap-2 hover:bg-slate-100"
                            >
                                <RotateCcw size={20} /> Try Again
                            </button>
                        </div>
                    )}

                    {won && (
                        <div className="absolute inset-0 flex flex-col items-center justify-center bg-yellow-500/80 text-white animate-in zoom-in">
                            <p className="text-4xl font-bold mb-2 text-center">Ninu Chakka! 🎉</p>
                            <p className="text-xl mb-4">You won!</p>
                            <button
                                onClick={(e) => { e.stopPropagation(); startGame(); }}
                                className="bg-white text-slate-900 px-6 py-3 rounded-full font-bold flex items-center gap-2 hover:bg-slate-100"
                            >
                                <RotateCcw size={20} /> Play Again
                            </button>
                        </div>
                    )}

                    <div className="absolute top-4 left-4 bg-black/30 text-white px-3 py-1 rounded-full font-mono font-bold">
                        {score}
                    </div>
                </div>

                <p className="text-center text-slate-500 dark:text-slate-400 text-sm mt-4">
                    Tap or Click to jump. Reach 10 to win!
                </p>
            </div>
        </div>
    );
}

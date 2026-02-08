"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login, signup } from "@/lib/api";

export default function Home() {
  const [isSignup, setIsSignup] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (isSignup) {
        await signup({ email, password });
      }
      await login({ email, password });
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden">
      {/* Animated Abstract Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800">
        {/* Animated Waves/Lines */}
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-0 left-0 w-full h-full">
            {/* Flowing Lines */}
            <svg className="absolute w-full h-full" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style={{ stopColor: '#60a5fa', stopOpacity: 0.8 }} />
                  <stop offset="100%" style={{ stopColor: '#93c5fd', stopOpacity: 0.2 }} />
                </linearGradient>
                <linearGradient id="grad2" x1="100%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style={{ stopColor: '#3b82f6', stopOpacity: 0.6 }} />
                  <stop offset="100%" style={{ stopColor: '#60a5fa', stopOpacity: 0.1 }} />
                </linearGradient>
              </defs>
              {/* Flowing curves */}
              <path
                d="M0,300 Q250,200 500,300 T1000,300 L1000,0 L0,0 Z"
                fill="url(#grad1)"
                className="animate-wave-slow"
              />
              <path
                d="M0,400 Q300,300 600,400 T1200,400 L1200,0 L0,0 Z"
                fill="url(#grad2)"
                className="animate-wave-slower"
              />
            </svg>
          </div>

          {/* Glowing Lines */}
          <div className="absolute top-20 left-10 w-96 h-1 bg-gradient-to-r from-transparent via-blue-400 to-transparent opacity-60 blur-sm animate-slide-right"></div>
          <div className="absolute top-40 right-20 w-64 h-1 bg-gradient-to-r from-transparent via-cyan-300 to-transparent opacity-50 blur-sm animate-slide-left"></div>
          <div className="absolute bottom-32 left-32 w-80 h-1 bg-gradient-to-r from-transparent via-blue-300 to-transparent opacity-40 blur-sm animate-slide-right-slow"></div>
          <div className="absolute top-1/2 right-10 w-72 h-1 bg-gradient-to-r from-transparent via-sky-400 to-transparent opacity-50 blur-sm animate-slide-left-slow"></div>
        </div>

        {/* Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900/50 via-transparent to-slate-900/30"></div>
      </div>

      {/* Content Container */}
      <div className="relative z-10 w-full max-w-md px-8">
        {/* Logo/Branding */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="flex items-center justify-center gap-3 mb-3">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center shadow-2xl shadow-blue-500/50">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-200 via-cyan-200 to-blue-300 bg-clip-text text-transparent">
              Todo App
            </h1>
          </div>
          <p className="text-blue-200/80 text-lg">Organize your tasks beautifully</p>
        </div>

        {/* Login Form */}
        <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl shadow-2xl p-8 animate-fade-in-delay">
          {/* Header */}
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-white mb-2">
              {isSignup ? "Create your account" : "Sign in to your account"}
            </h2>
            <p className="text-blue-200 text-sm">
              {isSignup ? "Already have an account? " : "Or "}
              <button
                onClick={() => {
                  setIsSignup(!isSignup);
                  setError("");
                }}
                className="text-cyan-300 hover:text-cyan-200 font-medium underline"
              >
                {isSignup ? "sign in" : "create a new account"}
              </button>
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email Input */}
            <div>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email address"
                required
                className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-lg text-white placeholder-blue-200/60 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
              />
            </div>

            {/* Password Input */}
            <div>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password (min 8 characters)"
                required
                minLength={8}
                className="w-full px-4 py-3 bg-white/20 backdrop-blur-sm border border-white/30 rounded-lg text-white placeholder-blue-200/60 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
              />
            </div>

            {/* Error Message */}
            {error && (
              <div className="rounded-lg bg-red-500/20 backdrop-blur-sm border border-red-400/50 p-3">
                <p className="text-sm text-red-200">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full px-4 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:from-blue-700 hover:to-cyan-700 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:ring-offset-2 focus:ring-offset-slate-900 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-lg shadow-blue-500/50"
            >
              {loading ? "Please wait..." : isSignup ? "Sign up" : "Sign in"}
            </button>
          </form>

          {/* Additional Info */}
          <div className="mt-6 text-center text-xs text-blue-200/60">
            <p>By continuing, you agree to our Terms & Privacy Policy</p>
          </div>
        </div>
      </div>

      {/* Bottom Gradient */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-slate-900 to-transparent"></div>

      <style jsx>{`
        @keyframes wave-slow {
          0%, 100% { transform: translateX(0) translateY(0); }
          50% { transform: translateX(-25px) translateY(-15px); }
        }
        @keyframes wave-slower {
          0%, 100% { transform: translateX(0) translateY(0); }
          50% { transform: translateX(25px) translateY(10px); }
        }
        @keyframes slide-right {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(200%); }
        }
        @keyframes slide-left {
          0% { transform: translateX(200%); }
          100% { transform: translateX(-100%); }
        }
        @keyframes slide-right-slow {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(200%); }
        }
        @keyframes slide-left-slow {
          0% { transform: translateX(200%); }
          100% { transform: translateX(-100%); }
        }
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .animate-wave-slow {
          animation: wave-slow 8s ease-in-out infinite;
        }
        .animate-wave-slower {
          animation: wave-slower 12s ease-in-out infinite;
        }
        .animate-slide-right {
          animation: slide-right 8s linear infinite;
        }
        .animate-slide-left {
          animation: slide-left 10s linear infinite;
        }
        .animate-slide-right-slow {
          animation: slide-right-slow 15s linear infinite;
        }
        .animate-slide-left-slow {
          animation: slide-left-slow 12s linear infinite;
        }
        .animate-fade-in {
          animation: fade-in 0.8s ease-out forwards;
        }
        .animate-fade-in-delay {
          animation: fade-in 0.8s ease-out 0.3s forwards;
          opacity: 0;
        }
      `}</style>
    </main>
  );
}

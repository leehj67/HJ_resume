"use client";

import { useRef, useCallback } from "react";
import Intro from "@/components/Intro";
import Hero from "@/components/Hero";
import Identity from "@/components/Identity";
import MainPortfolio from "@/components/MainPortfolio";

export default function Home() {
  const heroRef = useRef<HTMLDivElement>(null);

  const handleIntroComplete = useCallback(() => {
    heroRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  return (
    <main className="min-h-screen bg-[#0a0a0a]">
      <Intro onComplete={handleIntroComplete} />
      <div ref={heroRef}>
        <Hero />
      </div>
      <Identity />
      <MainPortfolio />
    </main>
  );
}

"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

const INTRO_TEXTS = [
  "정보를 찾고 계신가요?",
  "하지만 원하는 답이 나오지 않나요?",
  "검색은 되지만, 답은 없습니다",
  "그 문제, 해결할 수 있습니다",
];

const INTRO_INTERVAL_MS = 2000;

interface IntroProps {
  onComplete: () => void;
}

export default function Intro({ onComplete }: IntroProps) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < INTRO_TEXTS.length - 1) {
      const timer = setTimeout(() => setIndex((i) => i + 1), INTRO_INTERVAL_MS);
      return () => clearTimeout(timer);
    }
    // 마지막 문장 이후 다음 섹션으로 스크롤
    const scrollTimer = setTimeout(onComplete, INTRO_INTERVAL_MS);
    return () => clearTimeout(scrollTimer);
  }, [index, onComplete]);

  return (
    <section className="relative flex min-h-screen w-full items-center justify-center bg-[#0a0a0a]">
      <div className="px-6 text-center md:px-12">
        <AnimatePresence mode="wait">
          <motion.p
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -15 }}
            transition={{
              duration: 0.6,
              ease: [0.4, 0, 0.2, 1],
            }}
            className="text-2xl font-light leading-relaxed text-white/95 sm:text-3xl md:text-4xl lg:text-5xl"
          >
            {INTRO_TEXTS[index]}
          </motion.p>
        </AnimatePresence>
      </div>
    </section>
  );
}

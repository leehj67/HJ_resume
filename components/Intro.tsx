"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface IntroBlock {
  title: string;
  subtitle: string | null;
  emphasized?: boolean;
}

const INTRO_BLOCKS: IntroBlock[] = [
  {
    title: "문제는 복잡하지 않습니다.",
    subtitle: "정리가 안 되어 있을 뿐입니다.",
  },
  {
    title: "데이터는 부족하지 않습니다.",
    subtitle: "활용이 안 될 뿐입니다.",
  },
  {
    title: "저는",
    subtitle: null,
  },
  {
    title: "복잡함을 구조로 바꾸고,",
    subtitle: "데이터를 결과로 만듭니다.",
    emphasized: true,
  },
];

const INTRO_INTERVAL_MS = 2200;

interface IntroProps {
  onComplete: () => void;
}

export default function Intro({ onComplete }: IntroProps) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (index < INTRO_BLOCKS.length) {
      const timer = setTimeout(() => setIndex((i: number) => i + 1), INTRO_INTERVAL_MS);
      return () => clearTimeout(timer);
    }
    // intro.png 표시 후 2.2초 뒤 다음 섹션으로 스크롤
    const scrollTimer = setTimeout(onComplete, INTRO_INTERVAL_MS);
    return () => clearTimeout(scrollTimer);
  }, [index, onComplete]);

  const isImageStep = index === INTRO_BLOCKS.length;
  const currentBlock = !isImageStep ? INTRO_BLOCKS[index] : null;

  return (
    <section className="relative flex min-h-screen w-full items-center justify-center bg-[#0a0a0a]">
      <div className="flex flex-col items-center justify-center px-6 text-center md:px-12">
        <AnimatePresence mode="wait">
          {currentBlock && (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 24, filter: "blur(8px)" }}
              animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              exit={{ opacity: 0, y: -12, filter: "blur(6px)" }}
              transition={{
                duration: 0.65,
                ease: [0.4, 0, 0.2, 1],
              }}
              className="flex flex-col gap-3"
            >
              <p
                className={
                  currentBlock.emphasized
                    ? "text-3xl font-medium leading-relaxed text-white sm:text-4xl md:text-5xl lg:text-6xl"
                    : "text-2xl font-light leading-relaxed text-white/95 sm:text-3xl md:text-4xl"
                }
              >
                {currentBlock.title}
              </p>
              {currentBlock.subtitle && (
                <p
                  className={
                    currentBlock.emphasized
                      ? "text-xl font-light text-white/90 sm:text-2xl md:text-3xl"
                      : "text-lg font-light text-white/75 sm:text-xl md:text-2xl"
                  }
                >
                  {currentBlock.subtitle}
                </p>
              )}
            </motion.div>
          )}
          {isImageStep && (
            <motion.div
              key="intro-image"
              initial={{ opacity: 0, scale: 0.95, filter: "blur(8px)" }}
              animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
              exit={{ opacity: 0, scale: 0.98, filter: "blur(6px)" }}
              transition={{
                duration: 0.8,
                ease: [0.4, 0, 0.2, 1],
              }}
              className="relative flex max-h-[70vh] w-full max-w-2xl items-center justify-center"
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src="/intro.png"
                alt=""
                className="max-h-[70vh] w-auto object-contain"
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </section>
  );
}

"use client";

import { motion } from "framer-motion";

export default function Hero() {
  return (
    <section className="relative flex min-h-screen w-full flex-col items-center justify-center overflow-hidden bg-gradient-to-b from-[#0a0a0a] via-[#111] to-[#0a0a0a]">
      <div className="flex flex-1 flex-col items-center justify-center px-6 py-16">
        {/* 프로필 이미지 - 먼저 등장 */}
        <motion.div
          initial={{ opacity: 0, scale: 0.92 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{
            duration: 0.8,
            ease: [0.4, 0, 0.2, 1],
            delay: 0.15,
          }}
          className="mb-12"
        >
          <div className="relative flex h-36 w-36 items-center justify-center overflow-hidden rounded-full bg-gradient-to-br from-[#1a1a2e] to-[#16213e] ring-2 ring-white/20 sm:h-44 sm:w-44">
            <span className="text-4xl font-light text-white/80">HJ</span>
          </div>
        </motion.div>

        {/* 헤드라인 */}
        <motion.h1
          initial={{ opacity: 0, y: 18 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{
            duration: 0.75,
            ease: [0.4, 0, 0.2, 1],
            delay: 0.5,
          }}
          className="mb-5 max-w-2xl text-center text-2xl font-medium leading-relaxed tracking-tight text-white sm:text-3xl md:text-4xl lg:text-5xl"
        >
          복잡한 문제를 구조로 바꾸고,
          <br />
          데이터로 결과를 만드는 엔지니어
        </motion.h1>

        {/* 서브 텍스트 */}
        <motion.p
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{
            duration: 0.65,
            ease: [0.4, 0, 0.2, 1],
            delay: 0.85,
          }}
          className="text-sm font-light tracking-[0.2em] text-white/55 sm:text-base"
        >
          Research · Data · Search · Engineering
        </motion.p>
      </div>
    </section>
  );
}

"use client";

import { motion } from "framer-motion";

export default function Hero() {
  return (
    <section className="relative flex min-h-screen w-full flex-col items-center justify-center overflow-hidden bg-gradient-to-b from-[#0a0a0a] via-[#111] to-[#0a0a0a]">
      <div className="flex flex-1 flex-col items-center justify-center px-6 py-16">
        {/* 프로필 이미지 - 먼저 등장 */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{
            duration: 0.8,
            ease: [0.4, 0, 0.2, 1],
            delay: 0.2,
          }}
          className="mb-10"
        >
          <div className="relative flex h-36 w-36 items-center justify-center overflow-hidden rounded-full bg-gradient-to-br from-[#1a1a2e] to-[#16213e] ring-2 ring-white/20 sm:h-44 sm:w-44">
            <span className="text-4xl font-light text-white/80">HJ</span>
          </div>
        </motion.div>

        {/* 메인 타이틀 */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{
            duration: 0.7,
            ease: [0.4, 0, 0.2, 1],
            delay: 0.6,
          }}
          className="mb-4 text-center text-3xl font-semibold tracking-tight text-white sm:text-4xl md:text-5xl"
        >
          RAG & 데이터 엔지니어
        </motion.h1>

        {/* 서브 문구 */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{
            duration: 0.7,
            ease: [0.4, 0, 0.2, 1],
            delay: 0.9,
          }}
          className="max-w-xl text-center text-base font-light leading-relaxed text-white/70 sm:text-lg md:text-xl"
        >
          검색을 &apos;되게&apos;가 아니라 &apos;맞게&apos; 만드는 사람
        </motion.p>
      </div>
    </section>
  );
}

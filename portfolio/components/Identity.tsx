"use client";

import { motion } from "framer-motion";

export default function Identity() {
  return (
    <section className="relative flex min-h-screen w-full items-center justify-center bg-[#0a0a0a]">
      <div className="mx-auto max-w-3xl px-6 text-center">
        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{
            duration: 0.8,
            ease: [0.4, 0, 0.2, 1],
          }}
          className="mb-6 text-xl font-medium leading-relaxed text-white sm:text-2xl md:text-3xl"
        >
          데이터를 이해하고,
          <br />
          검색과 시스템으로 문제를 해결합니다
        </motion.p>
        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{
            duration: 0.8,
            ease: [0.4, 0, 0.2, 1],
            delay: 0.2,
          }}
          className="text-sm font-light text-white/50 sm:text-base"
        >
          연구 · 데이터 처리 · 검색 · 엔지니어링
        </motion.p>
      </div>
    </section>
  );
}

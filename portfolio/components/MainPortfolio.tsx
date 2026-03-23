"use client";

import { motion } from "framer-motion";

export default function MainPortfolio() {
  return (
    <motion.section
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
      className="relative min-h-screen w-full"
    >
      <iframe
        src="/index.html"
        title="포트폴리오 상세"
        className="h-screen w-full border-0"
        style={{ minHeight: "100vh" }}
      />
    </motion.section>
  );
}

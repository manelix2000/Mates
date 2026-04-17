export const t = {
  appTitle: "Mates 4t ESO — Pràctica",
  chooseTopic: "Tria un tema per començar:",
  progress: (done: number, total: number) =>
    total > 0 ? `${done}/${total} exercicis fets` : `${done} exercicis fets`,
  stats: (correct: number, wrong: number) => `${correct} ben fets · ${wrong} errats`,
  reset: "Reiniciar",
  resetConfirm: (topic: string) =>
    `Segur que vols reiniciar el progrés de «${topic}»? Perdràs el registre dels exercicis fets.`,
  check: "Comprova",
  next: "Següent",
  back: "Tornar als temes",
  correct: "Correcte!",
  incorrect: "Incorrecte",
  correctAnswerPrefix: "La resposta correcta és ",
  correctAnswerSuffix: ".",
  resolution: "Resolució pas a pas",
  allDoneTitle: "Ja has fet tots els exercicis d'aquest tema!",
  allDoneBody: "Pots tornar-hi a començar quan vulguis per repassar.",
  restart: "Tornar a començar",
  loading: "Carregant…",
  errorLoading: "No s'han pogut carregar els exercicis.",
  noOptionSelected: "Selecciona una opció per comprovar.",
};

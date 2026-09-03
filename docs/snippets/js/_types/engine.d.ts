// A minimal declaration of the part of `@idfkit/engine` the browser-simulation examples use.
//
// The engine is built and published from a separate repository and is deliberately not a
// dependency of this one: it carries 51 MB of WebAssembly, it pins one EnergyPlus release, and
// it is not reachable through the shared install name (FR-070). Adding it to package.json to
// type-check two examples would put all of that in every contributor's node_modules.
//
// This file is therefore a stand-in, and it is a weaker check than the rest of this tree: it
// catches an example calling a method this shape does not have, and it cannot catch the engine
// renaming one. T147 replaces it by type-checking against the engine's published types in CI,
// which is the check FR-071 and SC-030 actually ask for.
declare module '@idfkit/engine' {
  export interface EnergyPlusRunResult {
    success: boolean;
    fatalError?: string;
    err?: { entries: readonly { type: string; message: string }[] };
    eso?: { variables: Map<string, unknown> };
  }

  export interface EnergyPlusRunOptions {
    idf: string;
    epw: string;
    files?: Record<string, string>;
  }

  export interface EnergyPlus {
    run(options: EnergyPlusRunOptions): Promise<EnergyPlusRunResult>;
    dispose(): void;
  }

  export function createEnergyPlus(options: { assetBaseUrl: string }): Promise<EnergyPlus>;
  export function expandObjects(idf: string): Promise<string>;
}

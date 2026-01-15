/// <reference types="vite/client" />

declare module 'roughjs' {
  export interface Options {
    roughness?: number
    bowing?: number
    stroke?: string
    strokeWidth?: number
    fill?: string
    fillStyle?: string
  }

  export interface RoughGenerator {
    rectangle(x: number, y: number, width: number, height: number, options?: Options): SVGElement
    circle(x: number, y: number, width: number, options?: Options): SVGElement
    line(x1: number, y1: number, x2: number, y2: number, options?: Options): SVGElement
    ellipse(x: number, y: number, width: number, height: number, options?: Options): SVGElement
    polygon(points: [number, number][], options?: Options): SVGElement
    path(path: string, options?: Options): SVGElement
  }

  export function svg(svg: SVGElement): RoughGenerator
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function isNumber(value: any) {
  return !isNaN(+value)
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function notEmpty(value: any) {
  return value.toString().length > 0
}

export function min(value: number, min_val: number) {
  return +value >= min_val
}

export function max(value: number, max_val: number) {
  return +value <= max_val
}

export function between(value: number, min_val: number, max_val: number) {
  return min(value, min_val) && max(value, max_val)
}

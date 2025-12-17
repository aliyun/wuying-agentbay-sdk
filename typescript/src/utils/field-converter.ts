/**
 * Utility functions for converting field names between different naming conventions
 */

/**
 * Converts a snake_case string to camelCase
 * @param str - The snake_case string to convert
 * @returns The camelCase version of the string
 * 
 * @example
 * ```typescript
 * snakeToCamel('window_id') // returns 'windowId'
 * snakeToCamel('user_name') // returns 'userName'
 * snakeToCamel('simple') // returns 'simple'
 * ```
 */
export function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

/**
 * Converts an object with snake_case keys to camelCase keys
 * @param obj - The object to convert
 * @returns A new object with camelCase keys
 * 
 * @example
 * ```typescript
 * const input = { window_id: 123, user_name: 'John', age: 30 };
 * const output = convertObjectKeys(input);
 * // output: { windowId: 123, userName: 'John', age: 30 }
 * ```
 */
export function convertObjectKeys<T = any>(obj: any): T {
  if (obj === null || obj === undefined) {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => convertObjectKeys(item)) as T;
  }

  if (typeof obj === 'object' && obj.constructor === Object) {
    const converted: any = {};
    for (const [key, value] of Object.entries(obj)) {
      const camelKey = snakeToCamel(key);
      converted[camelKey] = convertObjectKeys(value);
    }
    return converted as T;
  }

  return obj;
}

/**
 * Converts window data from backend snake_case format to frontend camelCase format
 * @param rawWindow - Raw window data from backend
 * @returns Converted window data with camelCase keys
 * 
 * @example
 * ```typescript
 * const raw = { window_id: 123, title: 'Calculator', pid: 456, pname: 'calc.exe' };
 * const converted = convertWindowData(raw);
 * // converted: { windowId: 123, title: 'Calculator', pid: 456, pname: 'calc.exe' }
 * ```
 */
export function convertWindowData(rawWindow: any): any {
  if (!rawWindow) return rawWindow;
  
  return convertObjectKeys(rawWindow);
}

/**
 * Converts an array of window data from backend format to frontend format
 * @param rawWindows - Array of raw window data from backend
 * @returns Array of converted window data with camelCase keys
 * 
 * @example
 * ```typescript
 * const rawList = [
 *   { window_id: 123, title: 'Calculator' },
 *   { window_id: 456, title: 'Notepad' }
 * ];
 * const converted = convertWindowList(rawList);
 * // converted: [
 * //   { windowId: 123, title: 'Calculator' },
 * //   { windowId: 456, title: 'Notepad' }
 * // ]
 * ```
 */
export function convertWindowList(rawWindows: any[]): any[] {
  if (!Array.isArray(rawWindows)) return [];
  
  return rawWindows.map(window => convertWindowData(window));
}

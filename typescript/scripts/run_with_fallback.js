'use strict'

const { existsSync } = require('fs')
const path = require('path')
const { spawnSync } = require('child_process')

const fallbackPackagesByBin = {
  tsup: ['tsup@8.5.0', 'typescript@4.9.5'],
  jest: ['jest@26.6.3', 'ts-jest@26.5.6', 'ts-node@10.9.2', 'typescript@4.9.5'],
  eslint: ['eslint@8.35.0'],
  prettier: ['prettier@2.8.4'],
  typedoc: ['typedoc@0.28.3', 'typescript@4.9.5'],
  tsc: ['typescript@4.9.5'],
  'ts-node': ['ts-node@10.9.2', 'typescript@4.9.5'],
}

function resolveLocalBinary(binName) {
  const suffix = process.platform === 'win32' ? '.cmd' : ''
  const localPath = path.join(__dirname, '..', 'node_modules', '.bin', `${binName}${suffix}`)
  return existsSync(localPath) ? localPath : null
}

function getNpxCommand() {
  return process.platform === 'win32' ? 'npx.cmd' : 'npx'
}

function runWithFallback(binName, pkgSpecifier, args, options = {}) {
  const localBinary = resolveLocalBinary(binName)

  if (localBinary) {
    // On Windows, use cmd.exe to execute .cmd files to avoid EINVAL errors
    if (process.platform === 'win32' && localBinary.endsWith('.cmd')) {
      return spawnSync('cmd.exe', ['/c', localBinary, ...args], {
        stdio: 'inherit',
        ...options,
      })
    }
    
    return spawnSync(localBinary, args, {
      stdio: 'inherit',
      ...options,
    })
  }

  const command = getNpxCommand()
  const packageSet = new Set([pkgSpecifier, ...(fallbackPackagesByBin[binName] ?? [])])
  const packageArgs = []
  for (const pkg of packageSet) {
    if (pkg) {
      packageArgs.push('-p', pkg)
    }
  }

  return spawnSync(command, ['--yes', ...packageArgs, binName, ...args], {
    stdio: 'inherit',
    ...options,
  })
}

if (require.main === module) {
  const [, , binName, pkgSpecifier, ...args] = process.argv
  if (!binName || !pkgSpecifier) {
    console.error('Usage: node scripts/run_with_fallback.js <binary> <package[@version]> [args...]')
    process.exit(1)
  }

  const result = runWithFallback(binName, pkgSpecifier, args)

  if (result.error) {
    console.error(result.error)
  }

  process.exit(result.status ?? 1)
}

module.exports = { runWithFallback }


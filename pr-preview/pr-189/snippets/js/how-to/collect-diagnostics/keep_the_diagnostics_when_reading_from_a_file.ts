// --8<-- [start:example]
import { loadIdfWithDiagnostics } from '@idfkit/core/node';

const { document, diagnostics } = await loadIdfWithDiagnostics('model.idf', {
  strict: false,
});
// --8<-- [end:example]

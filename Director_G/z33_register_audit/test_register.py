"""Regression checks for the primary citation and heading attached to a Z33 judgment."""
import unittest

from check_register import PUBLIC_BASE, check_judgment


class JudgmentTest(unittest.TestCase):
    def test_issued_heading_and_primary_citation(self):
        row = {
            'id': 'B1-05-03', 'paper': 'B1', 'paper_file_page': '39',
            'kind': 'Corollary', 'number': '3', 'name': 'electrical resistance and full reconstruction',
            'status': 'PROOF_NOT_ADJACENT',
        }
        stem = 'B1_What_Does_an_Observation_Identify_A_Synthesis_with_Supporting_Notes'
        paper = f'PAPERS/{stem}/{stem}.pdf'
        heading = 'Corollary 3 electrical resistance and full reconstruction'
        body = (f'Issued status `{row["status"]}`.\n\n'
                f'[Assembled B1, p. 39]({PUBLIC_BASE}edition/{paper}#page=39)')
        check_judgment(row, paper, heading, body)
        cases = {
            'heading for a different statement': (heading.replace('Corollary 3', 'Theorem 999'), body),
            'different PDF in the same paper directory': (heading, body.replace(f'/{stem}.pdf', '/missing.pdf')),
            'wrong printed page': (heading, body.replace('p. 39]', 'p. 40]')),
            'wrong linked page': (heading, body.replace('#page=39', '#page=40')),
            'conflicting issued statuses': (heading, body + '\nIssued status `RESTATEMENT`.'),
        }
        for scenario, (changed_heading, changed_body) in cases.items():
            with self.subTest(scenario=scenario), self.assertRaises(ValueError):
                check_judgment(row, paper, changed_heading, changed_body)


if __name__ == '__main__':
    unittest.main()

# Contributing

Keep the guides portable across institutions, disciplines, operating systems, and assistants. Do not add personal paths, course launch URLs, credentials, or student records.

## Documentation changes

Maintain the Markdown guides in `guidelines/` and their equivalent text resources in `resources/text/` together. Preserve assessed requirements and distinguish optional activities from graded work. Keep references and assignment templates self-contained. Label platform observations with their verification date and scope.

## Example changes

Edit the solved notebook in `instructor/`, retaining stable criterion IDs when updating a deployed assignment. Update the manifest and rubric if the learning contract changes. Run the example's validator to regenerate and verify its student preview. Record observed scores; do not copy a result from another assignment.

Run `python scripts/check_repository.py` and the affected native nbgrader validator before proposing changes. Keep temporary execution logs, outputs, private course details, and secrets out of commits. Use synthetic test submissions.

A passing local validator does not prove a live Vocareum deployment or a returned Canvas grade. Document any platform testing separately.

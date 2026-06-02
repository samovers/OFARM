# CP5 conformance fixture plan

Positive fixtures validate all promoted manifest-honesty schemas and examples.

Negative fixtures check:

1. read-only hint conflicts with state-affecting effect class;
2. manifest omits external egress;
3. runtime-passed readiness claim has no runtime evidence;
4. manifest flags do not grant authority;
5. static validation cannot be represented as runtime readiness.

The CP5 runner validates positive examples and checks the negative fixtures for expected policy failures.

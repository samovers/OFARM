"""Typed meaning equality and numerical set predicates below explicit gates.

The selected expectation is an independently supplied DOMAIN expectation, not a
foreign source record or evidence producer format. Exact source adapters and
owner checks must establish it. No API here accepts a pass/admission Boolean.
"""
from common import *
from intrinsics import Intrinsics,nonempty_interval
from runtime_support import exact,error,number,interval_outcome

class MeaningComparisons:
    def __init__(self):self.intrinsics=Intrinsics();self.values=self.intrinsics.values
    def row(self,claim,selected):
        errors=[]
        for side,value in [('claim',claim),('selected',selected)]:
            errors.extend({**e,'pointer':'/'+side+e['pointer']} for e in self.intrinsics.check(value)['errors'])
            if not isinstance(value,dict) or value.get('form')!='ATOM':errors.append(error('SELECTED_ROW_REQUIRES_ATOM','/'+side))
        if errors:return self.result(errors,[])
        comparisons=[]
        for field in ['definition','scope','body']:
            same=exact(claim[field],selected[field]);comparisons.append({'pointer':'/'+field,'equal':same})
            if not same:errors.append(error('SELECTED_ROW_MEANING_MISMATCH','/'+field))
        return self.result(errors,comparisons)
    def quantity(self,claim,selected,operator,selected_operator,threshold,selected_threshold):
        """Value comparison starts only after role/material/basis/posture gates.

        Threshold inputs are owned scalar quantities. Their authority, lexical
        provenance, conversion and role are separately selected upstream. This
        routine neither converts a unit nor interprets a regulatory threshold.
        """
        errors=self.values.quantity_context_errors(claim,selected)
        for side,value in [('threshold',threshold),('selectedThreshold',selected_threshold)]:
            errors.extend({**e,'pointer':'/'+side+e['pointer']} for e in self.values.value_errors('scalarQuantity',value))
        if operator!=selected_operator:errors.append(error('SELECTED_OPERATOR_MISMATCH','/operator'))
        if not exact(threshold,selected_threshold):errors.append(error('SELECTED_THRESHOLD_MISMATCH','/threshold'))
        if errors:return self.result(errors,[])
        value=claim['value'];selected_value=selected['value']
        if not exact(value,selected_value):errors.append(error('SELECTED_QUANTITY_VALUE_OR_QUALIFICATION_MISMATCH','/value'))
        for key in ['quantityKind','unit']:
            if value['quantity'][key]!=threshold[key]:errors.append(error('THRESHOLD_QUANTITY_CONTEXT_MISMATCH','/threshold/'+key))
        if value['qualifier']!='EXACT':errors.append(error('NONEXACT_QUANTITY_REQUIRES_SELECTED_ADMISSIBLE_SET','/value/qualifier'))
        if errors:return self.result(errors,[])
        decimal=value['quantity']['decimal'];math=interval_outcome(operator,decimal,decimal,threshold['decimal'])
        result=self.result(math['errors'],[])
        if not math['errors']:result['conditionalMathematicalOutcome']=math['outcome']
        return result
    def criterion(self,claim,selected,selected_mapping_context=None):
        """C04 exact set logic after all owned selected-meaning/context gates.

        Complete equality includes criterion, immutable method/source/subject
        roles, unit profile, provenance, nonnegative/mapping/bounds, qualification
        and threshold. Independently selected meaning is required; a string such
        as METHOD_NONNEGATIVE_BELOW_LOQ cannot execute or establish that rule.
        Alleged outcome is deliberately compared to the computed value last.
        """
        c=copy.deepcopy(claim);s=copy.deepcopy(selected)
        if not isinstance(c,dict) or not isinstance(s,dict):return self.result([error('CRITERION_REQUIRES_TYPED_ATOMS','')],[])
        if c.get('definition')!=DEFINITION_PREFIX+'C04' or s.get('definition')!=DEFINITION_PREFIX+'C04':return self.result([error('CRITERION_REQUIRES_C04','/definition')],[])
        # Validate claimed outcome before excluding it from the expectation.
        errors=self.intrinsics.check(c)['errors']+self.intrinsics.check(s)['errors']
        if errors:return self.result(errors,[])
        alleged=c['body']['allegedOutcome'];c['body']['allegedOutcome']=s['body']['allegedOutcome']
        gate=self.row(c,s)
        if gate['errors']:return gate
        body=c['body'];operand=body['operand'];threshold=body['threshold']
        if operand['resultKind']=='ABSENT_PENDING':outcome='INDETERMINATE'
        else:
            interval=operand['admissibleValues'];lo=interval['lower'];hi=interval['upper'];bounds=(lo.get('decimal'),hi.get('decimal'));inclusive=(lo.get('inclusive',True),hi.get('inclusive',True))
            operand_quantity=operand.get('quantity',operand.get('limit'))
            thresholds=[threshold['lower'],threshold['upper']] if body['operator']=='BETWEEN' else [threshold]
            if operand_quantity:
                for t in thresholds:
                    for key in ['quantityKind','unit','unitProfile']:
                        if not exact(operand_quantity[key],t[key]):errors.append(error('CRITERION_QUANTITY_CONTEXT_MISMATCH','/body/threshold/'+key))
            else:
                # Coded/qualitative mappings need the exact selected mapping
                # interpretation to establish the target quantity kind/unit.
                # Equality alone does not manufacture that interpretation.
                mapping=selected_mapping_context
                if not isinstance(mapping,dict) or set(mapping)!={'mappingBinding','quantityKind','unit','unitProfile'}:
                    errors.append(error('MAPPING_TARGET_QUANTITY_CONTEXT_REQUIRED','/body/operand/mappingBinding'))
                else:
                    errors.extend(self.values.value_errors('binding',mapping['mappingBinding']))
                    errors.extend(self.values.value_errors('binding',mapping['unitProfile']))
                    if not exact(mapping['mappingBinding'],operand['mappingBinding']):errors.append(error('SELECTED_MAPPING_BINDING_MISMATCH','/body/operand/mappingBinding'))
                    for t in thresholds:
                        for key in ['quantityKind','unit','unitProfile']:
                            if not exact(mapping[key],t[key]):errors.append(error('MAPPED_QUANTITY_CONTEXT_MISMATCH','/body/threshold/'+key))
            if errors:return self.result(errors,[])
            if body['operator']=='BETWEEN':
                # Set containment in a closed/open range and disjointness are
                # evaluated directly. Combining independent tri-values would
                # be unsound for an impossible/empty acceptance range.
                lower,upper=number(threshold['lower']['decimal']),number(threshold['upper']['decimal']);a=None if bounds[0] is None else number(bounds[0]);z=None if bounds[1] is None else number(bounds[1]);li,ui=threshold['lowerInclusive'],threshold['upperInclusive']
                inside=(a is not None and (a>lower or (a==lower and (li or not inclusive[0])))) and (z is not None and (z<upper or (z==upper and (ui or not inclusive[1]))))
                disjoint=(z is not None and (z<lower or (z==lower and not(inclusive[1] and li)))) or (a is not None and (a>upper or (a==upper and not(inclusive[0] and ui))))
                outcome='SATISFIED' if inside else 'NOT_SATISFIED' if disjoint else 'INDETERMINATE'
            else:
                math=interval_outcome(body['operator'],*bounds,threshold['decimal'],*inclusive)
                if math['errors']:return self.result(math['errors'],[])
                outcome=math['outcome']
        if alleged!=outcome:errors.append(error('ALLEGED_CRITERION_OUTCOME_MISMATCH','/body/allegedOutcome',expected=outcome))
        result=self.result(errors,gate['comparisons']);result['conditionalMathematicalOutcome']=outcome
        return result
    @staticmethod
    def result(errors,comparisons):return {'scope':'INDEPENDENTLY_SELECTED_DOMAIN_MEANING_AND_MATH_ONLY','disposition':'COMPARISON_FAILED' if errors else 'OWNED_COMPARISONS_SATISFIED','errors':errors,'comparisons':comparisons,'requiredUpstreamRoles':['ACTUAL_SOURCE_ADAPTER_COMPARISONS','EXACT_SOURCE_RESOLUTION_AND_ELIGIBLE_USE','SELECTED_DOMAIN_DEFINITION_PROVENANCE'],'next':'Conjoin these comparisons with the coordinator mandatory gates; never treat this result as an admitted fact.'}
